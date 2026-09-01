---
name: artifact-generator
description: "High-fidelity dynamic document and web presentation generator. Compiles structured JSON/Markdown into pixel-perfect, ATS-friendly PDFs (via Typst) and standalone responsive HTML web dossiers composable with publish-to-trycloudflare across multiple audience presets (executive, technical, graphically_rich)."
user-invocable: true
allowed-tools: Bash(*)
---

# Dynamic Artifact Generator Skill

A modular, zero-dependency document compilation and web presentation generator for Multica agents. Transforms structured data (JSON Resume, Technical Briefs, Executive Reports, Specs) into dual-delivery formats:
- **Print-Ready Pixel-Perfect PDF & Vector SVG**: Sub-50ms deterministic compilation powered by the standalone, statically linked Typst engine.
- **Interactive Public Web (HTML)**: Responsive, standalone single-page dossiers styled with Tailwind CSS, dark/light theme switching, and print styles, composable with `publish-to-trycloudflare`.

---

## 1. Architectural Model & Dual Delivery

```text
                           [ Structured Input ]
                  (JSON Resume / Research Data / Specs)
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
   [ Typst Typesetting Engine ]                  [ Standalone Web Engine ]
   - Sub-50ms static musl binary                 - Tailwind CSS responsive SPA
   - Embedded fonts (no system deps)             - Dark/Light mode theme switch
   - Tagged ATS-compliant PDF                    - Print-to-PDF styles
   - Multi-page vector SVG export                - Zero external server deps
           │                                                 │
           ▼                                                 ▼
   [ PDF & SVG Artifacts ]                       [ Interactive HTML Dossier ]
           │                                                 │
           │                                      [ publish-to-trycloudflare ]
           ▼                                                 ▼
  Local / Attachment Delivery                       Public Preview URL
```

---

## 2. Audience Presets & Styling Profiles

The skill provides three curated audience presets:

| Preset | Target Audience & Use Case | Visual Characteristics | Typography |
| :--- | :--- | :--- | :--- |
| **`executive`** | Board reports, senior leadership dossiers, ATS-friendly resumes | Single-column formal hierarchy, conservative whitespace, subtle horizontal rules, full ATS compatibility | `Libertinus Serif` |
| **`technical`** | Architecture specs, engineering deep dives, system benchmarks | Condensed margins (1.4cm), structured two-column key-value tables, monospace tags, system impact bullets | `DejaVu Sans` + `DejaVu Sans Mono` |
| **`graphically_rich`** | Public portfolios, project showcases, metric summaries | Accent banners, stat highlight callout boxes, colored skill badges, modern card containers | `DejaVu Sans` + Indigo/Sky Accents |

---

## 3. CLI Command Reference

### Bootstrapping Typst Engine
The skill automatically bootstraps the standalone static musl Typst binary upon first run, or you can invoke it directly:

```bash
skills/artifact-generator/scripts/ensure_typst.sh
```

### Generating Artifacts

```bash
# Render all formats (PDF, SVG, and HTML) using the Executive preset
python3 skills/artifact-generator/scripts/render_artifact.py \
  --data examples/resume_data.json \
  --preset executive \
  --format all \
  --output-dir ./dist

# Render high-density technical PDF only
python3 skills/artifact-generator/scripts/render_artifact.py \
  --data examples/resume_data.json \
  --preset technical \
  --format pdf \
  --output-dir ./dist

# Render graphically rich presentation with SVG vector exports
python3 skills/artifact-generator/scripts/render_artifact.py \
  --data examples/resume_data.json \
  --preset graphically_rich \
  --format all \
  --output-dir ./dist
```

### CLI Arguments

- `--data <path>`: Required path to the JSON input file.
- `--preset`: Audience preset (`executive`, `technical`, `graphically_rich`). Default: `executive`.
- `--format`: Output format (`pdf`, `svg`, `html`, `all`). Default: `all`.
- `--output-dir`: Output destination directory. Default: `./dist`.

---

## 4. Serving Public Web Previews with `publish-to-trycloudflare`

To present an interactive web dossier to human stakeholders without deployment infrastructure:

```bash
# 1. Start the local artifact preview server in the background (serving port 8080)
skills/artifact-generator/scripts/serve_preview.sh 8080 ./dist &

# 2. Expose via Cloudflare outbound zero-trust tunnel using the companion skill
multica skill run publish-to-trycloudflare --port 8080
```

The resulting `https://*.trycloudflare.com` URL provides immediate access to the interactive HTML presentation, complete with dynamic theme switching and client-side print-to-PDF capabilities.

---

## 5. Directory Layout

```text
skills/artifact-generator/
├── SKILL.md
├── bin/                          # Standalone static Typst musl binary (auto-downloaded)
├── scripts/
│   ├── ensure_typst.sh           # Auto-installer for standalone Typst binary
│   ├── render_artifact.py        # Core CLI orchestrator
│   └── serve_preview.sh          # Local preview web server
├── templates/
│   ├── executive.typ             # Executive / Professional Typst template
│   ├── technical.typ             # Contextually Dense / Technical Typst template
│   └── graphically_rich.typ      # Graphically Rich Typst template
├── examples/
│   └── resume_data.json          # Standard JSON Resume input dataset
├── references/
│   └── RESEARCH_BRIEF.md         # Full empirical evaluation, MFCM, and benchmarks
└── tests/
    └── test_artifact_pipeline.py # End-to-end regression tests
```

---

## 6. Testing

Run automated end-to-end tests:

```bash
python3 skills/artifact-generator/tests/test_artifact_pipeline.py
```
