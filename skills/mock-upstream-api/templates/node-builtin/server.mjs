// Zero-dependency Node.js Upstream Mock Server
// Native node:http, zero npm install, runs instantly on Node 18+
import http from 'node:http';
import url from 'node:url';

const PORT = parseInt(process.env.PORT || '4000', 10);
const RATE_LIMIT_MAX = parseInt(process.env.RATE_LIMIT_MAX || '10', 10);
const RATE_LIMIT_WINDOW_MS = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '10000', 10);
const DEFAULT_PAGE_SIZE = 10;

// Generic In-Memory Seed Items (Customizable)
const items = Array.from({ length: 50 }, (_, i) => ({
  id: `mock-item-${String(i + 1).padStart(4, '0')}`,
  name: `Sample Item ${i + 1}`,
  status: ['active', 'pending', 'completed', 'archived'][i % 4],
  amount: Number((10.0 + (i * 7.5) % 500).toFixed(2)),
  createdAt: new Date(1700000000000 + i * 86400000).toISOString()
}));

// Sliding Window Rate Limiter
const requestLogs = [];

function checkRateLimit(req, res) {
  const now = Date.now();
  while (requestLogs.length > 0 && requestLogs[0] <= now - RATE_LIMIT_WINDOW_MS) {
    requestLogs.shift();
  }

  const remaining = Math.max(0, RATE_LIMIT_MAX - requestLogs.length);
  const resetSec = Math.ceil((requestLogs.length > 0 ? (requestLogs[0] + RATE_LIMIT_WINDOW_MS - now) : RATE_LIMIT_WINDOW_MS) / 1000);

  res.setHeader('X-RateLimit-Limit', RATE_LIMIT_MAX);
  res.setHeader('X-RateLimit-Remaining', remaining);
  res.setHeader('X-RateLimit-Reset', resetSec);

  const force429 = req.headers['x-mock-status'] === '429' || req.url.includes('simulate_429=true');
  if (force429 || requestLogs.length >= RATE_LIMIT_MAX) {
    res.setHeader('Retry-After', resetSec || 1);
    res.writeHead(429, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please back off and retry.',
      retry_after_seconds: resetSec || 1,
      limit: RATE_LIMIT_MAX,
      window_seconds: Math.round(RATE_LIMIT_WINDOW_MS / 1000)
    }));
    return false;
  }

  requestLogs.push(now);
  return true;
}

const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = (parsedUrl.pathname || '/').replace(/\/+$/, '') || '/';
  const query = parsedUrl.query;

  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Mock-Status, X-Mock-Delay');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Rate Limiting Guard
  if (!checkRateLimit(req, res)) return;

  // Simulated Latency
  const delayMs = parseInt(query.delay || req.headers['x-mock-delay'] || '0', 10);
  if (delayMs > 0) {
    await new Promise(resolve => setTimeout(resolve, delayMs));
  }

  // Health Check
  if (pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
    return;
  }

  // Collection Endpoints: GET /items, GET /api/items
  const isCollection = pathname === '/items' || pathname === '/api/items' || pathname === '/api/data';
  if (isCollection && req.method === 'GET') {
    let limit = parseInt(query.limit || query.size || DEFAULT_PAGE_SIZE, 10);
    limit = Math.min(Math.max(limit, 1), 100);

    let offset = 0;
    if (query.offset !== undefined) {
      offset = Math.max(0, parseInt(query.offset, 10));
    } else if (query.page !== undefined) {
      const page = Math.max(1, parseInt(query.page, 10));
      offset = (page - 1) * limit;
    } else if (query.cursor) {
      try {
        offset = parseInt(Buffer.from(query.cursor, 'base64').toString('ascii'), 10) || 0;
      } catch (e) {
        offset = 0;
      }
    }

    let filtered = [...items];
    if (query.status) {
      filtered = filtered.filter(i => String(i.status).toLowerCase() === String(query.status).toLowerCase());
    }
    if (query.q) {
      const q = String(query.q).toLowerCase();
      filtered = filtered.filter(i => JSON.stringify(i).toLowerCase().includes(q));
    }

    const total = filtered.length;
    const paginated = filtered.slice(offset, offset + limit);
    const hasMore = offset + limit < total;
    const nextOffset = hasMore ? offset + limit : null;
    const nextCursor = nextOffset !== null ? Buffer.from(String(nextOffset)).toString('base64') : null;

    res.setHeader('X-Total-Count', total);
    res.setHeader('X-Has-More', hasMore ? 'true' : 'false');
    if (nextCursor) res.setHeader('X-Next-Cursor', nextCursor);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      data: paginated,
      pagination: {
        total,
        count: paginated.length,
        offset,
        limit,
        page: Math.floor(offset / limit) + 1,
        total_pages: Math.ceil(total / limit),
        has_more: hasMore,
        next_cursor: nextCursor
      }
    }));
    return;
  }

  // Item by ID: GET /items/:id or GET /api/items/:id
  const itemMatch = pathname.match(/^(?:\/api)?\/items\/([^/]+)$/);
  if (itemMatch && req.method === 'GET') {
    const id = itemMatch[1];
    const item = items.find(i => String(i.id) === id);
    if (!item) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not Found', message: `Item ${id} not found` }));
      return;
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ data: item }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Route Not Found', path: pathname }));
});

server.listen(PORT, () => {
  console.log(`🚀 Zero-dep Mock API listening on http://127.0.0.1:${PORT}`);
  console.log(`   Collection: GET http://127.0.0.1:${PORT}/api/items?page=1&limit=10`);
  console.log(`   Rate Limit: ${RATE_LIMIT_MAX} requests / ${RATE_LIMIT_WINDOW_MS / 1000}s`);
});
