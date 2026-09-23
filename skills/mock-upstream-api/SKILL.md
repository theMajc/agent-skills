---
name: mock-upstream-api
description: "Rapidly scaffolds a mock third-party upstream API (Node.js zero-dep, Express, json-server, or FastAPI) with built-in pagination, 429 rate-limiting, and error injection from an entity shape in seconds. Invocable via `/mock-api` or when asked to 'mock api', 'mock upstream', 'scaffold fake service', or 'mock 3rd party api'."
user-invocable: true
allowed-tools: Bash(*)
---

# Mock Upstream API Generator (`/mock-api`)

Instantly scaffold an in-memory upstream HTTP server or route handler for live coding exercises, integration tests, or decoupled frontend/backend development when a third-party specification is provided without a running upstream system.

---

## 1. Core Invariants & Guardrails

1. **Plumbing Only (Zero Business Logic Invariant):**
   - Must only generate generic transport infrastructure: CRUD/collection routes, pagination envelopes, rate limiting headers, HTTP status simulation, and latency delays.
   - **Never inject exercise-specific business logic, transformation algorithms, or domain calculation rules.** Preserves the integrity of live-coding assessments and clean architectural boundaries.

2. **Built-In Pagination by Default (Not Opt-In):**
   - Every collection endpoint immediately supports standard query patterns: `?limit=N&offset=N`, `?page=N&limit=N`, and cursor-based tokens `?cursor=...`.
   - Returns standard envelope `{ data: [...], pagination: { total, count, offset, limit, page, total_pages, has_more, next_cursor } }` plus standard response headers (`X-Total-Count`, `X-Has-More`, `X-Next-Cursor`).

3. **Built-In Simulated Rate Limiting & 429 Responses by Default:**
   - Active sliding window rate limiter emitting `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
   - Returns `HTTP 429 Too Many Requests` with `Retry-After: N` when threshold is exceeded.
   - Deterministic test triggers: header `X-Mock-Status: 429` or query parameter `?simulate_429=true`.

4. **Sub-Minute Setup Time:**
   - Zero-dependency Node.js template (`node:http`) runs instantly without waiting for `npm install`.
   - Scaffold script generates complete runnable servers directly from schema definitions in < 5 seconds.

---

## 2. Fast Scaffolding CLI (`scripts/scaffold_mock.py`)

Generate a customized mock server from entity definitions or JSON schemas:

```bash
# 1. Zero-dependency Node.js server from field definitions (Default)
python3 skills/mock-upstream-api/scripts/scaffold_mock.py \
  --entity customer \
  --fields "id:uuid,name:string,email:string,status:string,balance:number,createdAt:datetime" \
  --count 50 \
  --port 4000 \
  --output ./mock-server.mjs

# 2. Run the generated server instantly
node ./mock-server.mjs
```

### Supported Generation Flavors

| Flavor | Flag | Runtime / Dependencies | Best For |
|---|---|---|---|
| **Node Built-in** *(Default)* | `--flavor node-builtin` | Native Node 18+ (`node:http`), **0 dependencies** | Live-coding exercises with time pressure (<5s setup) |
| **Express JS** | `--flavor express-js` | Node.js + `express` + `cors` | Existing Express/Node repositories |
| **FastAPI** | `--flavor fastapi` | Python 3 + `fastapi` + `uvicorn` | Python backends and data pipelines |
| **JSON Server** | `--flavor json-server` | `json-server` + custom middleware | Instant REST API from static JSON |

---

## 3. Ready-to-Use Boilerplate Templates

Pre-built, ready-to-run templates are located in `skills/mock-upstream-api/templates/`:

- **Zero-Dependency Node.js**: [`templates/node-builtin/server.mjs`](templates/node-builtin/server.mjs)
  ```bash
  node skills/mock-upstream-api/templates/node-builtin/server.mjs
  ```
- **Express.js (JavaScript)**: [`templates/express/server.js`](templates/express/server.js)
  ```bash
  node skills/mock-upstream-api/templates/express/server.js
  ```
- **Express.js (TypeScript)**: [`templates/express/server.ts`](templates/express/server.ts)
  ```bash
  npx ts-node skills/mock-upstream-api/templates/express/server.ts
  ```
- **JSON Server**: [`templates/json-server/db.json`](templates/json-server/db.json) & [`templates/json-server/middleware.js`](templates/json-server/middleware.js)
  ```bash
  npx json-server --watch templates/json-server/db.json --middlewares templates/json-server/middleware.js --port 4000
  ```
- **Python FastAPI**: [`templates/fastapi/main.py`](templates/fastapi/main.py)
  ```bash
  uvicorn skills.mock-upstream-api.templates.fastapi.main:app --port 4000
  ```

---

## 4. API Endpoints & Request Contract

Every generated mock API implements the following contract:

### 1. Paginated Collection: `GET /api/{entity}s` (or `/{entity}s`)
**Query Parameters:**
- `page` (int, 1-indexed) & `limit` (int, default 10)
- `offset` (int, 0-indexed) & `limit` (int)
- `cursor` (base64 string)
- `status` (string filter)
- `q` (full-text search query)
- `delay` (simulated latency in ms)
- `simulate_429=true` (forces immediate 429 response)

**Response (HTTP 200):**
```json
{
  "data": [
    {
      "id": "mock-item-0001",
      "name": "Sample Item 1",
      "status": "active",
      "amount": 10.0,
      "createdAt": "2023-11-15T00:00:00.000Z"
    }
  ],
  "pagination": {
    "total": 50,
    "count": 1,
    "offset": 0,
    "limit": 10,
    "page": 1,
    "total_pages": 5,
    "has_more": true,
    "next_cursor": "MTA="
  }
}
```

### 2. Single Entity: `GET /api/{entity}s/:id`
**Response (HTTP 200):**
```json
{
  "data": {
    "id": "mock-item-0001",
    "name": "Sample Item 1",
    "status": "active",
    "amount": 10.0,
    "createdAt": "2023-11-15T00:00:00.000Z"
  }
}
```

### 3. Rate Limit Exceeded (HTTP 429)
**Headers:**
- `X-RateLimit-Limit: 10`
- `X-RateLimit-Remaining: 0`
- `X-RateLimit-Reset: 8`
- `Retry-After: 8`

**Body:**
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

## 5. References

- [Pagination Design Patterns](references/PAGINATION_PATTERNS.md)
- [Rate Limiting & Error Simulation](references/RATE_LIMIT_PATTERNS.md)
