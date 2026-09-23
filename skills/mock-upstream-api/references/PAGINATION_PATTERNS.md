# Pagination Patterns Reference

Standard pagination design patterns supported by `mock-upstream-api` for upstream mock services.

---

## 1. Supported Pagination Styles

### Pattern A: Offset / Limit (Default)
Query parameters:
- `?limit=10` (or `?size=10`)
- `?offset=20`

Response payload envelope:
```json
{
  "data": [ ... ],
  "pagination": {
    "total": 50,
    "count": 10,
    "offset": 20,
    "limit": 10,
    "page": 3,
    "total_pages": 5,
    "has_more": true,
    "next_cursor": "MzA="
  }
}
```

### Pattern B: Page / Page Size
Query parameters:
- `?page=2`
- `?limit=10` (or `?size=10`)

Calculated offset:
`offset = (page - 1) * limit`

### Pattern C: Cursor / Token Based
Query parameters:
- `?cursor=MTA=`
- `?limit=10`

Header and envelope contract:
- Base64-encoded position token: `Buffer.from(String(nextOffset)).toString('base64')`
- Response header: `X-Next-Cursor: MTA=`
- Response header: `X-Has-More: true`

---

## 2. Response Headers Contract

| Header | Description | Example |
|---|---|---|
| `X-Total-Count` | Total available records matching filter | `50` |
| `X-Has-More` | Boolean flag indicating subsequent page availability | `true` |
| `X-Next-Cursor` | Opaque base64 cursor for fetching next page | `MTA=` |
| `Link` | RFC 5988 web link header (optional) | `<https://api.example.com/items?page=2>; rel="next"` |
