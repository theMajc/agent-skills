# agent-skills

Personal agent skills monorepo for Multica agents and autonomous development workflows.

This repository hosts production-ready, reusable agent skills following the standard agent skills format (`SKILL.md` + helper scripts).

## Catalog of Skills

| Skill | Description | Path |
|---|---|---|
| [`publish-to-trycloudflare`](skills/publish-to-trycloudflare/) | Publishes a local development port to a public TryCloudflare URL (`https://*.trycloudflare.com`) using an outbound zero-trust tunnel. | [`skills/publish-to-trycloudflare`](skills/publish-to-trycloudflare/) |
| [`token-reducer`](skills/token-reducer/) | Minimizes agent token usage via sub-3ms RTK terminal compaction, transparent hooks, and Repomix AST codebase context packing. | [`skills/token-reducer`](skills/token-reducer/) |

---

## Installation & Multica Import

To import a skill from this monorepo into your Multica workspace:

```bash
# Import publish-to-trycloudflare
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/publish-to-trycloudflare --output json

# Import token-reducer
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/token-reducer --output json
```

To bind the imported skill to an agent:

```bash
multica agent skills add <agent-id> --skill-ids <skill-id> --output json
```

## Structure

```text
agent-skills/
├── README.md
└── skills/
    ├── publish-to-trycloudflare/
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── ensure_cloudflared.sh
    │       ├── publish_start.sh
    │       ├── publish_stop.sh
    │       └── publish_status.sh
    └── token-reducer/
        ├── SKILL.md
        ├── README.md
        ├── references/
        │   ├── BENCHMARK_MATRIX.md
        │   └── OPERATIONAL_RECIPES.md
        ├── scripts/
        │   ├── agy_hook_rewrite.py
        │   ├── ensure_rtk.sh
        │   ├── compact_run.sh
        │   ├── pack_context.sh
        │   └── compact_fallback.py
        └── tests/
            └── test_orchestrator.py
```

## License

MIT
