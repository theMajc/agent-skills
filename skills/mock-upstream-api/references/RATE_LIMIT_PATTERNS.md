# Rate Limit & Error Simulation Patterns Reference

Standard rate limiting and failure simulation specifications implemented by `mock-upstream-api`.

---

## 1. Rate Limiting Headers & Behavior

Every request returns rate limit telemetry in the HTTP response headers:

| Header | Description | Default / Example |
|---|---|---|
| `X-RateLimit-Limit` | Maximum number of allowed requests in current window | `10` |
| `X-RateLimit-Remaining` | Remaining requests available before hitting 429 | `9` |
| `X-RateLimit-Reset` | Seconds until rate limit quota resets | `10` |
| `Retry-After` | Included on HTTP 429 response indicating wait time | `5` |

---

## 2. HTTP 429 Response Schema

When the sliding window capacity is exceeded (or when triggered manually), the server returns HTTP 429:

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please back off and retry.",
  "retry_after_seconds": 8,
  "limit": 10,
  "window_seconds": 10
}
```

---

## 3. Dynamic Simulation Controls

You can test upstream failure handling and client retry loops deterministically without waiting for sliding windows to fill up:

### Force HTTP 429
- Request Header: `X-Mock-Status: 429`
- Query Parameter: `?simulate_429=true`

### Simulated Network Latency
- Request Header: `X-Mock-Delay: 250` (in milliseconds)
- Query Parameter: `?delay=250` (in milliseconds)
