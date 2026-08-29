---
name: publish-to-trycloudflare
description: "Publishes a local development port to a public TryCloudflare URL (`https://*.trycloudflare.com`) using an outbound zero-trust tunnel. Use when asked to 'deploy to public dev', 'publish to trycloudflare', 'share preview link', or 'stop/unpublish preview'."
user-invocable: true
allowed-tools: Bash(*)
---

# Publish to TryCloudflare

Publish a local development service to an external, publicly accessible TryCloudflare Quick Tunnel (`https://*.trycloudflare.com`) with zero network ingress configuration, NAT traversal, or Cloudflare credentials required.

---

## 1. When to Use

Use this skill when:
- Asked to **"deploy to public dev"**, **"publish to trycloudflare"**, or **"share preview link"**.
- A member wants an external reviewer or client to interact with a locally running web app, API, or frontend prototype.
- Asked to **"stop preview"**, **"unpublish preview"**, or check active preview links.

Do **not** use for production deployments or long-term production domains; TryCloudflare quick tunnels are ephemeral preview environments without SLA guarantees.

---

## 2. Architecture & Turn Boundary Safety

TryCloudflare tunnels must survive across Multica agent turns:
- **Process Decoupling:** Tunnels are launched as detached background services using `persistent-service-supervisor` (`run_detached.sh` with `setsid` and `nohup`), ensuring they are not terminated when the subshell turn exits.
- **Synchronous Verification:** The start script synchronously scrapes the assigned `https://*.trycloudflare.com` URL from tunnel logs and performs an active WAN health check (`curl`) before returning.
- **Runtime Tracking:** State, PIDs, and logs are tracked in `.multica/runtime/` (`services.json`, `pids/`, `logs/`).

---

## 3. Workflow & Directives

### Step 1: Verify Local Server Is Running
Before establishing a public tunnel, verify that the local service is actually running and listening on the intended port:

```bash
# Check if port is active (e.g. port 3000)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://127.0.0.1:3000
```
- If the port is unresponsive or connection is refused, **start the local service first** (e.g. via `run_detached.sh <app-name> "<start-cmd>" --port <port>`).
- Do not create a tunnel pointing to a dead port.

### Step 2: Publish Local Port to TryCloudflare
Run the start script with the target port:

```bash
# Path to script from workspace root or skill directory
skills/publish-to-trycloudflare/scripts/publish_start.sh <port>
```

The script:
1. Ensures `cloudflared` binary is present (via `ensure_cloudflared.sh`).
2. Detaches the tunnel process named `preview-<port>` via `run_detached.sh`.
3. Monitors the logs until Cloudflare assigns a `*.trycloudflare.com` domain.
4. Performs a synchronous WAN HTTP probe to confirm the public URL is reachable.
5. Emits JSON output to stdout:
   ```json
   {"url": "https://random-subdomain.trycloudflare.com", "port": 3000, "service": "preview-3000"}
   ```

### Step 3: Inspect Active Tunnels
To list all active tunnels and their URLs:

```bash
skills/publish-to-trycloudflare/scripts/publish_status.sh
```

### Step 4: Stop a Preview Tunnel
When the preview session is complete or the user asks to stop/unpublish:

```bash
# Stop by port or service name
skills/publish-to-trycloudflare/scripts/publish_stop.sh 3000
# or
skills/publish-to-trycloudflare/scripts/publish_stop.sh preview-3000
```

---

## 4. Reporting Delivery in Issue Comments

When publishing a preview link, deliver the result in your issue comment following Multica guidelines:
- **Clickable Web Link:** Provide the public `https://*.trycloudflare.com` URL as a markdown link.
- **Do NOT link local filesystem paths:** Mention local log paths only as inline code.
- **Include Teardown Command:** Supply the exact `publish_stop.sh <port>` command.

### Example Handoff Format:
```markdown
### 🌐 Public Preview Available
- **Public URL:** [https://example-subdomain.trycloudflare.com](https://example-subdomain.trycloudflare.com)
- **Local Port:** `3000`
- **Service Name:** `preview-3000`
- **Status:** Verified reachable via WAN probe

To stop the tunnel:
```bash
skills/publish-to-trycloudflare/scripts/publish_stop.sh 3000
```
```
