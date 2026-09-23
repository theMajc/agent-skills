// Express.js Upstream Mock Server Boilerplate
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = parseInt(process.env.PORT || '4000', 10);
const RATE_LIMIT_MAX = parseInt(process.env.RATE_LIMIT_MAX || '10', 10);
const RATE_LIMIT_WINDOW_MS = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '10000', 10);

app.use(cors());
app.use(express.json());

// In-Memory Seed Store
const items = Array.from({ length: 50 }, (_, i) => ({
  id: `mock-item-${String(i + 1).padStart(4, '0')}`,
  name: `Sample Item ${i + 1}`,
  status: ['active', 'pending', 'completed', 'archived'][i % 4],
  amount: Number((10.0 + (i * 7.5) % 500).toFixed(2)),
  createdAt: new Date(1700000000000 + i * 86400000).toISOString()
}));

// Rate Limiting Sliding Window State
const requestLogs = [];

app.use((req, res, next) => {
  const now = Date.now();
  while (requestLogs.length > 0 && requestLogs[0] <= now - RATE_LIMIT_WINDOW_MS) {
    requestLogs.shift();
  }

  const remaining = Math.max(0, RATE_LIMIT_MAX - requestLogs.length);
  const resetSec = Math.ceil((requestLogs.length > 0 ? (requestLogs[0] + RATE_LIMIT_WINDOW_MS - now) : RATE_LIMIT_WINDOW_MS) / 1000);

  res.setHeader('X-RateLimit-Limit', RATE_LIMIT_MAX);
  res.setHeader('X-RateLimit-Remaining', remaining);
  res.setHeader('X-RateLimit-Reset', resetSec);

  const force429 = req.headers['x-mock-status'] === '429' || req.query.simulate_429 === 'true';
  if (force429 || requestLogs.length >= RATE_LIMIT_MAX) {
    res.setHeader('Retry-After', resetSec || 1);
    return res.status(429).json({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please back off and retry.',
      retry_after_seconds: resetSec || 1,
      limit: RATE_LIMIT_MAX,
      window_seconds: Math.round(RATE_LIMIT_WINDOW_MS / 1000)
    });
  }

  requestLogs.push(now);
  next();
});

// Latency Simulation Middleware
app.use(async (req, res, next) => {
  const delayMs = parseInt(req.query.delay || req.headers['x-mock-delay'] || '0', 10);
  if (delayMs > 0) {
    await new Promise(resolve => setTimeout(resolve, delayMs));
  }
  next();
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// GET /api/items (Paginated)
app.get(['/items', '/api/items'], (req, res) => {
  let limit = parseInt(req.query.limit || req.query.size || '10', 10);
  limit = Math.min(Math.max(limit, 1), 100);

  let offset = 0;
  if (req.query.offset !== undefined) {
    offset = Math.max(0, parseInt(req.query.offset, 10));
  } else if (req.query.page !== undefined) {
    const page = Math.max(1, parseInt(req.query.page, 10));
    offset = (page - 1) * limit;
  } else if (req.query.cursor) {
    try {
      offset = parseInt(Buffer.from(req.query.cursor, 'base64').toString('ascii'), 10) || 0;
    } catch (e) {
      offset = 0;
    }
  }

  let filtered = [...items];
  if (req.query.status) {
    filtered = filtered.filter(i => String(i.status).toLowerCase() === String(req.query.status).toLowerCase());
  }
  if (req.query.q) {
    const q = String(req.query.q).toLowerCase();
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

  res.json({
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
  });
});

// GET /api/items/:id
app.get(['/items/:id', '/api/items/:id'], (req, res) => {
  const item = items.find(i => String(i.id) === req.params.id);
  if (!item) {
    return res.status(404).json({ error: 'Not Found', message: `Item ${req.params.id} not found` });
  }
  res.json({ data: item });
});

// POST /api/items (Create)
app.post(['/items', '/api/items'], (req, res) => {
  const newItem = {
    id: `mock-item-${String(items.length + 1).padStart(4, '0')}`,
    ...req.body,
    createdAt: new Date().toISOString()
  };
  items.unshift(newItem);
  res.status(201).json({ data: newItem });
});

app.listen(PORT, () => {
  console.log(`🚀 Express Mock Server listening on http://127.0.0.1:${PORT}`);
  console.log(`   Collection: GET http://127.0.0.1:${PORT}/api/items?page=1&limit=10`);
});
