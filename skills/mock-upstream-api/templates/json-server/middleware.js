// json-server custom middleware
// Injects 429 rate limiting, Retry-After header, and pagination meta
const RATE_LIMIT_MAX = parseInt(process.env.RATE_LIMIT_MAX || '10', 10);
const RATE_LIMIT_WINDOW_MS = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '10000', 10);
const requestLogs = [];

module.exports = (req, res, next) => {
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
};
