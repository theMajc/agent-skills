# agent-skills

Personal agent skills monorepo for Multica agents and autonomous development workflows.

This repository hosts production-ready, reusable agent skills following the standard agent skills format (`SKILL.md` + helper scripts).

## Catalog of Skills

| Skill | Description | Path |
|---|---|---|
| [`publish-to-trycloudflare`](skills/publish-to-trycloudflare/) | Publishes a local development port to a public TryCloudflare URL (`https://*.trycloudflare.com`) using an outbound zero-trust tunnel. | [`skills/publish-to-trycloudflare`](skills/publish-to-trycloudflare/) |

---

## Installation & Multica Import

To import a skill from this monorepo into your Multica workspace:

```bash
# Import publish-to-trycloudflare
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/publish-to-trycloudflare --output json
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
    └── publish-to-trycloudflare/
        ├── SKILL.md
        └── scripts/
            ├── ensure_cloudflared.sh
            ├── publish_start.sh
            ├── publish_stop.sh
            └── publish_status.sh
```

## License

MIT
