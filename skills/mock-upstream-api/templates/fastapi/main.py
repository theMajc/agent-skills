# Python FastAPI Mock Server Boilerplate
import base64
import os
import time
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Mock Upstream API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = int(os.environ.get("PORT", "4000"))
RATE_LIMIT_MAX = int(os.environ.get("RATE_LIMIT_MAX", "10"))
RATE_LIMIT_WINDOW_SEC = int(os.environ.get("RATE_LIMIT_WINDOW_SEC", "10"))
request_logs = []

# Seed items
ITEMS = [
    {
        "id": f"mock-item-{i + 1:04d}",
        "name": f"Sample Item {i + 1}",
        "status": ["active", "pending", "completed", "archived"][i % 4],
        "amount": round(10.0 + (i * 7.5) % 500, 2),
        "createdAt": f"2023-11-{(i % 28) + 1:02d}T00:00:00.000Z"
    }
    for i in range(50)
]

@app.middleware("http")
async def rate_limit_and_latency_middleware(request: Request, call_next):
    now = time.time()
    global request_logs
    request_logs = [ts for ts in request_logs if ts > now - RATE_LIMIT_WINDOW_SEC]

    remaining = max(0, RATE_LIMIT_MAX - len(request_logs))
    reset_sec = int(RATE_LIMIT_WINDOW_SEC - (now - request_logs[0])) if request_logs else RATE_LIMIT_WINDOW_SEC

    # Check simulated delay
    delay_str = request.query_params.get("delay") or request.headers.get("x-mock-delay") or "0"
    try:
        delay = float(delay_str) / 1000.0
        if delay > 0:
            time.sleep(delay)
    except ValueError:
        pass

    force_429 = request.headers.get("x-mock-status") == "429" or request.query_params.get("simulate_429") == "true"
    if force_429 or len(request_logs) >= RATE_LIMIT_MAX:
        from fastapi.responses import JSONResponse
        headers = {
            "X-RateLimit-Limit": str(RATE_LIMIT_MAX),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(max(1, reset_sec)),
            "Retry-After": str(max(1, reset_sec)),
        }
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too Many Requests",
                "message": "Rate limit exceeded. Please back off and retry.",
                "retry_after_seconds": max(1, reset_sec),
                "limit": RATE_LIMIT_MAX,
                "window_seconds": RATE_LIMIT_WINDOW_SEC,
            },
            headers=headers
        )

    request_logs.append(now)
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_MAX)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(max(1, reset_sec))
    return response

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/items")
@app.get("/api/items")
def list_items(
    page: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[str] = Query(None),
    status: Optional[str] = None,
    q: Optional[str] = None,
    response: Response = None
):
    calculated_offset = 0
    if offset is not None:
        calculated_offset = offset
    elif page is not None:
        calculated_offset = (page - 1) * limit
    elif cursor:
        try:
            calculated_offset = int(base64.b64decode(cursor.encode()).decode())
        except Exception:
            calculated_offset = 0

    filtered = ITEMS
    if status:
        filtered = [i for i in filtered if str(i.get("status", "")).lower() == status.lower()]
    if q:
        filtered = [i for i in filtered if q.lower() in str(i).lower()]

    total = len(filtered)
    paginated = filtered[calculated_offset : calculated_offset + limit]
    has_more = (calculated_offset + limit) < total
    next_offset = calculated_offset + limit if has_more else None
    next_cursor = base64.b64encode(str(next_offset).encode()).decode() if next_offset is not None else None

    if response:
        response.headers["X-Total-Count"] = str(total)
        response.headers["X-Has-More"] = "true" if has_more else "false"
        if next_cursor:
            response.headers["X-Next-Cursor"] = next_cursor

    return {
        "data": paginated,
        "pagination": {
            "total": total,
            "count": len(paginated),
            "offset": calculated_offset,
            "limit": limit,
            "page": (calculated_offset // limit) + 1,
            "total_pages": (total + limit - 1) // limit if limit > 0 else 1,
            "has_more": has_more,
            "next_cursor": next_cursor
        }
    }

@app.get("/items/{item_id}")
@app.get("/api/items/{item_id}")
def get_item(item_id: str):
    for item in ITEMS:
        if str(item.get("id")) == str(item_id):
            return {"data": item}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 FastAPI Mock Server starting on http://127.0.0.1:{PORT}")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
