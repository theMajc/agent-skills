# agent-skills

Personal agent skills monorepo for Multica agents and autonomous development workflows.

This repository hosts production-ready, reusable agent skills following the standard agent skills format (`SKILL.md` + helper scripts).

## Catalog of Skills

| Skill | Description | Path |
|---|---|---|
| [`artifact-generator`](skills/artifact-generator/) | High-fidelity dynamic PDF and responsive web dossier generation via Typst and Tailwind across multiple audience presets. | [`skills/artifact-generator`](skills/artifact-generator/) |
| [`candidate-employer-due-diligence`](skills/candidate-employer-due-diligence/) | Dual-mode candidate employer due diligence pipeline (Quick Sanity Check & Deep Multi-Stage Due Diligence with Multica stage barriers & subagents). | [`skills/candidate-employer-due-diligence`](skills/candidate-employer-due-diligence/) |
| [`candidate-employer-deep-diligence`](skills/candidate-employer-deep-diligence/) | Deep multi-stage due diligence pipeline with native Multica stage barrier fan-out/fan-in and decoupled evidence consolidation. | [`skills/candidate-employer-deep-diligence`](skills/candidate-employer-deep-diligence/) |
| [`decompose`](skills/decompose/) | Fast structured-breakdown ritual (entities → data flow → edge cases → interface contract) for any non-trivial coding task before writing code, with a generated Mermaid diagram and judgment-driven (not fixed-list) edge-case identification. | [`skills/decompose`](skills/decompose/) |
| [`mock-upstream-api`](skills/mock-upstream-api/) | Rapid mock upstream API generator (zero-dep Node, Express, json-server, FastAPI) with built-in pagination, 429 rate-limit simulation, and failure injection. | [`skills/mock-upstream-api`](skills/mock-upstream-api/) |
| [`publish-to-trycloudflare`](skills/publish-to-trycloudflare/) | Publishes a local development port to a public TryCloudflare URL (`https://*.trycloudflare.com`) using an outbound zero-trust tunnel. | [`skills/publish-to-trycloudflare`](skills/publish-to-trycloudflare/) |
| [`token-reducer`](skills/token-reducer/) | Minimizes agent token usage via sub-3ms RTK terminal compaction, transparent hooks, and Repomix AST codebase context packing. | [`skills/token-reducer`](skills/token-reducer/) |
| [`verify-ai-output`](skills/verify-ai-output/) | Post-generation verification protocol (/verify) producing falsifiable edge-case checklists — scoped to the function's actual domain, not a fixed category list — with dual handled/not-handled status and remediation patches. | [`skills/verify-ai-output`](skills/verify-ai-output/) |

---

## Installation & Multica Import

To import a skill from this monorepo into your Multica workspace:

```bash
# Import mock-upstream-api
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/mock-upstream-api --output json

# Import artifact-generator
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/artifact-generator --output json

# Import publish-to-trycloudflare
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/publish-to-trycloudflare --output json

# Import token-reducer
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/token-reducer --output json

# Import decompose
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/decompose --output json

# Import verify-ai-output
multica skill import --url github.com/theMajc/agent-skills/tree/main/skills/verify-ai-output --output json
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
    ├── token-reducer/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── references/
    │   │   ├── BENCHMARK_MATRIX.md
    │   │   └── OPERATIONAL_RECIPES.md
    │   ├── scripts/
    │   │   ├── agy_hook_rewrite.py
    │   │   ├── ensure_rtk.sh
    │   │   ├── compact_run.sh
    │   │   ├── pack_context.sh
    │   │   └── compact_fallback.py
    │   └── tests/
    │       └── test_orchestrator.py
    └── verify-ai-output/
        ├── SKILL.md
        ├── templates/
        │   └── verification_matrix.md
        ├── examples/
        │   └── example_verification.md
        └── tests/
            └── test_verify_skill.py
```

## License

MIT
