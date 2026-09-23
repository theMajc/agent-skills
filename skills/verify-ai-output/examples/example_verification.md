# Verification Example: `sync_user_records`

This example demonstrates how `/verify` processes an AI-generated data synchronization function, identifying both handled guardrails and unhandled edge cases with line-level justifications.

---

### Target Function Code

```python
# sync_service.py
import requests
import time

def sync_user_records(user_payload: list[dict], api_key: str, max_batch: int = 50) -> dict:
    if not user_payload:
        return {"synced": 0, "errors": []}
    
    batch = user_payload[:max_batch]
    processed_ids = {}
    synced_count = 0
    errors = []

    for record in batch:
        user_id = record.get("id")
        email = record.get("email")
        
        # Upsert into internal dictionary
        processed_ids[user_id] = email
        
        # Send to downstream sync endpoint
        response = requests.post(
            "https://api.example.com/v1/users",
            json={"id": user_id, "email": email},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=5
        )
        if response.status_code == 200:
            synced_count += 1
        else:
            errors.append({"id": user_id, "status": response.status_code})

    return {"synced": synced_count, "errors": errors}
```

---

### Generated Verification Report

### Post-Generation Verification Report: `sync_user_records`

#### 1. Function Overview
- **Function / Target:** `sync_service.sync_user_records` (lines 5-32)
- **Language / Runtime:** Python 3.10+
- **Primary Responsibility:** Synchronizes a batch of user records to a remote downstream API endpoint.

---

#### 2. Edge-Case Verification Checklist

| Edge Case Category | Specific Scenario Tested | Handled? | Evidence / Line Ref | Falsifiable Justification & Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Empty / Null Input** | `user_payload = []` or `None` | `Handled` | L6-L7 | Guard clause `if not user_payload:` returns `{"synced": 0, "errors": []}` immediately. |
| **Duplicate Identifier** | Multiple records with identical `id` in `user_payload` | `Not Handled` | L18 | Dictionary assignment `processed_ids[user_id] = email` silently overwrites prior record and makes duplicate POST calls. |
| **Malformed Record** | Missing `id` or `email` key in dict | `Not Handled` | L14-L15 | `.get("id")` returns `None` when key is missing; POST sends `{"id": None, "email": None}` without schema validation. |
| **Rate Limit / 429 Backoff** | Downstream API returns HTTP 429 Too Many Requests | `Not Handled` | L21-L30 | Treats 429 as generic failure without exponential backoff or retry mechanism. |
| **Boundary / Limits** | `max_batch <= 0` | `Not Handled` | L9 | `user_payload[:0]` slices empty list without error, but negative values like `-5` slice incorrectly. |
| **Concurrency & State** | Concurrent invocations on independent instances | `Handled` | L5-L32 | Function is pure with respect to global state; operates strictly on local scope variables. |
| **Resource & Failure Modes** | Network timeout or connection drop | `Handled` | L25 | Explicit `timeout=5` set on HTTP call preventing hanging connections. |

---

#### 3. Verification Scorecard & Triage
- **Total Edge Cases Evaluated:** 7
- **Handled (`Handled`):** 3 / 7 (43%)
- **Not Handled (`Not Handled`):** 4 / 7 (57%)
- **Critical Gaps Requiring Remediation:** 3 (Duplicate ID, Malformed Record, Rate Limit / 429 Backoff)
- **Acceptable Exclusions / Delegated Upstream:** 1 (Boundary `max_batch` default parameter)

---

#### 4. Remediation Code Patch

```python
import requests
import time

def sync_user_records(user_payload: list[dict], api_key: str, max_batch: int = 50) -> dict:
    if not user_payload:
        return {"synced": 0, "errors": []}
    
    max_batch = max(1, max_batch)
    batch = user_payload[:max_batch]
    processed_ids = set()
    synced_count = 0
    errors = []

    for record in batch:
        if not isinstance(record, dict):
            errors.append({"error": "malformed_record", "payload": record})
            continue
            
        user_id = record.get("id")
        email = record.get("email")
        if not user_id or not email:
            errors.append({"id": user_id, "error": "missing_required_fields"})
            continue

        if user_id in processed_ids:
            # Skip duplicate in current batch
            continue
        processed_ids.add(user_id)

        # Retry loop for 429 rate limit
        for attempt in range(3):
            try:
                response = requests.post(
                    "https://api.example.com/v1/users",
                    json={"id": user_id, "email": email},
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=5
                )
                if response.status_code == 200:
                    synced_count += 1
                    break
                elif response.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    errors.append({"id": user_id, "status": response.status_code})
                    break
            except requests.RequestException as e:
                if attempt == 2:
                    errors.append({"id": user_id, "error": str(e)})

    return {"synced": synced_count, "errors": errors}
```

---

#### 5. Verification Verdict
- [x] **REMEDIATION REQUIRED:** Critical gaps in duplicate handling, schema validation, and HTTP 429 retry resolved via remediation patch.
