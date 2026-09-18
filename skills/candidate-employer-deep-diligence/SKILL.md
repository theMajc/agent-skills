---
name: candidate-employer-deep-diligence
description: "Rigorous, multi-agent deep due diligence pipeline for candidate employers. Enforces Multica Stage Barrier (`--stage N`) Fan-Out/Fan-In and parallel subagent orchestration across 4 decoupled pillars: Financial Viability, Layoff History, Culture/WLB, and Tech Stack Architecture. Produces Master Due Diligence Dossiers with anchored scoring and Reverse-Interview Playbooks."
user-invocable: true
---

# Candidate Employer Deep Due Diligence Skill

A specialized, high-integrity research pipeline for high-stakes career transitions, offer evaluations, and executive/senior engineering moves. Enforces formal decoupled stage barriers across financial health, layoff vulnerability, operational culture, and technical architecture.

---

## 1. Core Invariants & Anti-Hallucination Guardrails

To protect candidates from joining distressed or toxic organizations, four non-negotiable invariants are enforced:

### 1. The Zero-Sugarcoating Invariant (Brutal Honesty)
- Corporate PR, self-published marketing blogs, sponsored "Best Places to Work" awards, and recruiter pitches are treated as **unverified claims ($cf = 0.10$)**.
- Red flags must **never be euphemized** (e.g., do not call "uncompensated 70-hour weeks" a "fast-paced entrepreneurial environment").
- High turnover, toxic management, or financial distress must be reported explicitly as a **Critical Risk**.

### 2. Strict Decoupling of Employer Health vs. Candidate Alignment
- **The Health Invariant**: The **Objective Employer & Role Health Scorecard** measures *only* factual business stability, financial runway, historical layoff risk, operating friction, and leadership sanity.
- **No Keyword / Fit Inflation**: Candidate skill overlap **must NEVER inflate or mask** company instability or poor culture.
- **Dual-Index Output**: Maintains two non-overlapping indexes:
  1. *Index 1: Objective Employer & Role Health (Macro Stability)*
  2. *Index 2: Candidate Match & Interview Positioning (Personal Alignment)*

### 3. Anti-Hollow-Orchestration & Stage Barrier Invariant
- Sub-issues or subagents are **real units of decoupled execution**, not decorative checklists.
- **Strictly Prohibited**:
  - Creating child sub-issues directly in `done` status without posted comments/evidence.
  - Creating child sub-issues and marking them `done` in the same turn without genuine worker delegation.
  - Bypassing stage barriers.
- Every research pillar must produce its own self-contained evidence payload before the parent synthesis begins.

### 4. The "Floor, Not Ceiling" Source Boundary
- Baseline inquiry categories are minimums; dynamically discover alternative high-signal sources when facing bot walls or paywalls (Google-indexed community snippets, SEC filings, WARN databases, Hacker News, Reddit `r/cscareerquestions`, `r/experienceddevs`).

---

## 2. Orchestration Protocols

### Protocol A: Native Multica Stage Barriers (`--stage N` Fan-Out / Fan-In)

When running within a Multica issue-tracking project, deep due diligence **MUST** leverage Multica's native stage barrier lifecycle:

```
[Parent Ticket: Due Diligence Audit] (Status: in_progress)
   │
   ├── Phase 1 (Scouting & Stage 1 Fan-Out):
   │      ├── Create Child 1: "Track 1: Financial & Business Health"        (--stage 1 --status todo --assignee-id <agent>)
   │      ├── Create Child 2: "Track 2: Layoff & Stability History"         (--stage 1 --status todo --assignee-id <agent>)
   │      ├── Create Child 3: "Track 3: Culture, WLB & Management Quality"  (--stage 1 --status todo --assignee-id <agent>)
   │      ├── Create Child 4: "Track 4: Role Scope & Architecture"          (--stage 1 --status todo --assignee-id <agent>)
   │      └── Create Child 5: "Stage 2: Master Dossier Synthesis"           (--stage 2 --status backlog --assignee-id <agent>)
   │      └── [Parent Turn Exits / Yields to Platform Scheduler]
   │
   ├── Phase 2 (Autonomous Worker Execution):
   │      ├── Worker 1 executes Track 1 → Posts comment to Child 1 → Sets Child 1 to 'done'
   │      ├── Worker 2 executes Track 2 → Posts comment to Child 2 → Sets Child 2 to 'done'
   │      ├── Worker 3 executes Track 3 → Posts comment to Child 3 → Sets Child 3 to 'done'
   │      └── Worker 4 executes Track 4 → Posts comment to Child 4 → Sets Child 4 to 'done'
   │
   └── Phase 3 (Server Stage Barrier Wakeup & Parent Fan-In Synthesis):
          ├── Multica Server detects all Stage 1 tasks terminal ('done') → Wakes Parent Assignee!
          ├── Parent Lead Agent ingests all 4 Child comment payloads
          ├── Parent Lead Agent synthesizes Master Employer Due Diligence Dossier
          ├── Posts Master Dossier to Parent Issue comment
          └── Sets Parent Issue status to 'in_review'
```

#### Exact Multica CLI Lifecycle Sequence:

1. **Lead Turn 1 (Scaffolding & Fan-Out)**:
   ```bash
   # 1. Mark parent in_progress
   multica issue status <parent-id> in_progress --no-start

   # 2. Fan-out Stage 1 parallel worker issues in todo
   multica issue create --title "Track 1: Financial & Business Health" --parent <parent-id> --project <project-id> --stage 1 --status todo --assignee-id <agent-id>
   multica issue create --title "Track 2: Layoff & Stability History" --parent <parent-id> --project <project-id> --stage 1 --status todo --assignee-id <agent-id>
   multica issue create --title "Track 3: Culture, WLB & Management Quality" --parent <parent-id> --project <project-id> --stage 1 --status todo --assignee-id <agent-id>
   multica issue create --title "Track 4: Role Scope & Architecture" --parent <parent-id> --project <project-id> --stage 1 --status todo --assignee-id <agent-id>

   # 3. Park Stage 2 synthesis issue in backlog
   multica issue create --title "Stage 2: Master Dossier Synthesis" --parent <parent-id> --project <project-id> --stage 2 --status backlog --assignee-id <agent-id>
   ```
   *Lead agent posts a brief kickoff comment to the parent ticket and cleanly ends turn.*

2. **Worker Turns (Parallel Independent Execution)**:
   Each child issue runs as an independent task:
   - Researches its dedicated pillar in depth.
   - Saves findings to `./trackN_findings.md`.
   - Posts findings to the child issue:
     ```bash
     multica issue comment add <child-id> --content-file "./trackN_findings.md"
     multica issue status <child-id> done --no-start
     rm ./trackN_findings.md
     ```

3. **Lead Turn 2 (Post-Barrier Wakeup & Master Synthesis)**:
   When all 4 Stage 1 tasks reach `done`, Multica automatically wakes the parent assignee:
   ```bash
   # 1. Verify all children
   multica issue children <parent-id> --output json

   # 2. Read findings from each child comment
   multica issue comment list <child-1-id> --roots-only --summary --compact --output json
   multica issue comment list <child-2-id> --roots-only --summary --compact --output json
   multica issue comment list <child-3-id> --roots-only --summary --compact --output json
   multica issue comment list <child-4-id> --roots-only --summary --compact --output json

   # 3. Synthesize Master Dossier, write to ./final_dossier.md, and post to parent
   multica issue comment add <parent-id> --content-file "./final_dossier.md"
   rm ./final_dossier.md

   # 4. Advance parent to in_review
   multica issue status <parent-id> in_review --no-start
   ```

---

### Protocol B: Standalone / Subagent Environment (`invoke_subagent` Fallback)

When running in a direct chat room or autonomous CLI environment without Multica issue tracking:

```
[Lead Synthesizer Agent]
   │
   ├── Step 1: Dispatch 4 Parallel Subagents (invoke_subagent in a single call)
   │      ├── Subagent 1: Role 'Financial Auditor' (Pillar 1 prompt & targets)
   │      ├── Subagent 2: Role 'Layoff & Stability Auditor' (Pillar 2 prompt & targets)
   │      ├── Subagent 3: Role 'Culture & WLB Auditor' (Pillar 3 prompt & targets)
   │      └── Subagent 4: Role 'Architecture & Tech Auditor' (Pillar 4 prompt & targets)
   │
   ├── Step 2: Reactive Wakeup on Subagent Deliverables (isolated contexts)
   │
   └── Step 3: Compile Master Dossier and Output Directly to User
```

---

## 3. The 4 Specialized Research Pillars & Minimum Baselines

### Pillar 1: Financial Viability & Business Health
*Goal: Determine if the company has the financial runway and business momentum to sustain long-term employment.*

* **Minimum Baseline Inquiries:**
  * **Public Companies**: Latest SEC 10-K / 10-Q filing (Revenue trajectory over 3 years, operating margins, free cash flow, debt obligations, and key disclosures in the "Risk Factors" section).
  * **Private / VC-Backed Startups**: Latest known funding round, valuation history, lead venture backers, estimated employee headcount growth/contraction, and estimated cash runway.
  * **Revenue Model & Market Exposure**: Customer concentration risk, macroeconomic sensitivity, and primary revenue engines.
* **Adaptive Discovery Fallbacks:**
  * If financial reports are private, search for news of down-rounds, debt financing, hiring freezes, customer churn in public trade publications, or SEC Form D filings.

### Pillar 2: Employment Stability & Layoff Track Record
*Goal: Assess job security, organizational volatility, and leadership retention.*

* **Minimum Baseline Inquiries:**
  * **Layoff History**: Query **Layoffs.fyi**, news archives, and state/provincial **WARN Act notices** (mandatory legal filings prior to mass layoffs) over the past 24–36 months.
  * **Restructuring & Pivot Cadence**: Frequency of re-organizations, executive departures (C-suite turnover), and business unit shutdowns.
  * **Hiring Velocity vs. Backfill Ratio**: Is the target role a net-new strategic expansion, or a high-turnover backfill replacing a departed employee?
* **Adaptive Discovery Fallbacks:**
  * Search GitHub contributor graphs of key company repos or public forum discussions for sudden drops in core engineering personnel.

### Pillar 3: Culture, Work-Life Balance & Management Quality
*Goal: Uncover the daily operational reality, on-call burdens, and employee psychological safety.*

* **Minimum Baseline Inquiries:**
  * **On-Call & Work Hours**: Look for data on weekly hours, after-hours expectations, on-call compensation, and incident response culture.
  * **Community Discourse Triangulation**: Search **Reddit** (`r/cscareerquestions`, `r/experienceddevs`, local tech subreddits), **Levels.fyi** work-life reviews, **Hacker News** discussions, and public Google-indexed discussions (`site:teamblind.com "<company>" wlb OR culture`).
  * **Remote / Flexibility Policy Stability**: Track record of sudden Return-to-Office (RTO) mandates or broken remote-work promises.
* **Walled-Garden Bypass Rule:**
  * Never fail on Glassdoor/Blind bot blocks. Search search-engine indexed snippets, developer communities, and cross-reference multiple independent developer opinions.

### Pillar 4: Role Scope, Tech Stack Health & Engineering Maturity
*Goal: Evaluate technical debt, engineering autonomy, tooling friction, and operational complexity.*

* **Minimum Baseline Inquiries:**
  * **Tech Stack Maturity & Complexity**: Core technologies, cloud infrastructure, CI/CD pipeline maturity, automated testing coverage, microservice sprawl vs monolith.
  * **Engineering Footprint**: Public GitHub organization activity, engineering blogs, tech conference talks, open-source contributions.
  * **Role Danger Signals**: Vague job responsibilities ("wear many hats" disguised as doing 3 roles), legacy system firefighting, or high on-call pager burden caused by fragile third-party integrations.

---

## 4. Anchored Quantitative Scoring Rubrics (A–F Thresholds)

To eliminate qualitative model drift across LLM tiers, assign letter grades using these strict anchored criteria:

### 1. Financial Stability & Runway
* **A (Exceptional)**: Publicly traded with >$500M annual revenue & positive net operating margins, OR private company with >$30M ARR and verified profitability / >36 months cash runway.
* **B (Stable / Disciplined)**: Private company with $5M–$30M ARR, verified recent tier-1 institutional funding (within 18 months), or operating at steady break-even in a resilient niche.
* **C (Moderate Risk / Thin Runway)**: Sub-$5M ARR with unverified cash runway, last funding round >24 months ago without declared profitability, or down-round in last 18 months.
* **D/F (High / Existential Risk)**: Active bankruptcy/restructuring, burning cash with <6 months runway, debt default, or massive customer revenue collapse.

### 2. Role & Org Stability (Layoff Risk)
* **A (Highly Secure)**: 0 recorded layoffs or WARN notices across past 36 months; stable C-suite/founder tenure (>3 years average); steady strategic headcount growth.
* **B (Standard Market Risk)**: 1 minor restructuring round (<10% headcount) during broader market correction, with transparent severance and no subsequent rounds; stable core engineering leadership.
* **C (Volatile / High Churn)**: Multiple layoff rounds (>15% total) in past 24 months, frequent executive turnover (VP/CTO leaving within <1 year), or recurring team re-organizations.
* **D/F (Severe Instability)**: Continuous rolling layoffs, WARN notice filings within last 90 days, widespread executive exodus, or abrupt department shuttering.

### 3. Work-Life Balance & Operational Culture
* **A (Sustainable / Healthy)**: Average reported workweek 35–42 hours; formal, compensated on-call rotation with low pager volume; clear psychological safety and high Glassdoor/Reddit sentiment.
* **B (Manageable Startup Pace)**: Average workweek 40–48 hours; standard sprint cycles; on-call rotation shared fairly across team with occasional production alerts.
* **C (High Burnout / Unhealthy On-Call)**: Regular 50+ hour weeks expected; uncompensated 24/7 on-call firefighting; frequent weekend escalations; negative sentiment regarding micromanagement.
* **D/F (Toxic / Severe Grindhouse)**: Systematic 60+ hour crunch culture; abusive management reviews; extreme turnover (>30% annual engineering churn); broken remote work commitments.

### 4. Tech Stack & Engineering Architecture
* **A (Modern, Robust & Disciplined)**: Cloud-native, clean CI/CD automated deployment pipelines, high test coverage, standard telemetry (OpenTelemetry/Datadog), low operational firefighting.
* **B (Pragmatic / Manageable Debt)**: Solid modern stack with some legacy technical debt or third-party integration maintenance; active refactoring roadmap and stable test automation.
* **C (High Complexity / Severe Debt)**: Fragile distributed systems / microservice sprawl with poor documentation; brittle third-party dependencies requiring frequent manual intervention; inadequate testing sandboxes.
* **D/F (Crippling Legacy / Architecture Failure)**: Unmaintained bespoke monoliths or broken architectures; zero automated CI/CD; frequent production data corruption or multi-hour outages.

---

## 5. Standardized Output Schema: Employer Due Diligence Dossier

All deep due diligence outputs must follow this standardized Markdown schema:

```markdown
# Employer Due Diligence Dossier: [Company Name]
**Target Role / Team:** [Role Title, if known]  
**Audit Date:** [YYYY-MM-DD]  
**Objective Health Verdict:** [🟢 HIGH CONFIDENCE STABILITY / 🟡 PROCEED WITH CAUTION / 🔴 SIGNIFICANT RISK]  
**Confidence Rating:** [High (80-100%) / Medium (50-79%) / Low (<50%)]

---

## 1. Objective Employer & Role Health Scorecard

| Dimension | Grade (A–F) | Anchored Key Metric | Risk Level |
| :--- | :---: | :--- | :---: |
| **1. Financial Stability & Runway** | [A/B/C/D/F] | [Hard ARR / runway / funding metric] | [Low / Med / High] |
| **2. Role & Org Stability (Layoff Risk)** | [A/B/C/D/F] | [WARN & layoff track record] | [Low / Med / High] |
| **3. Work-Life Balance & Culture** | [A/B/C/D/F] | [Hours / on-call burden / sentiment] | [Low / Med / High] |
| **4. Tech Stack & Engineering Health** | [A/B/C/D/F] | [Architecture & operational complexity] | [Low / Med / High] |

### Objective TL;DR Verdict
[3–4 concise sentences detailing the objective truth regarding business longevity, layoff vulnerability, and operational friction—completely independent of candidate preferences.]

---

## 2. Candidate Alignment & Positioning Index (Optional / JD-Specific)

| Match Dimension | Score / Alignment | Key Factor |
| :--- | :---: | :--- |
| **Technical Stack Fit** | [High / Med / Low] | [Overlap with candidate competencies] |
| **Seniority & Scope Calibration** | [Matched / Under / Over] | [IC vs Tech Lead vs Management scope] |
| **Career Trajectory Leverage** | [High / Med / Low] | [Resume value of this role & company] |

---

## 3. Risk & Flag Matrix

### 🔴 Critical Red Flags (Dealbreakers)
- **[Flag Title]**: [Explanation backed by cited evidence].

### 🟡 Yellow Flags (Require Direct Verification)
- **[Flag Title]**: [Explanation backed by cited evidence].

### 🟢 Verified Strengths (Selling Points)
- **[Strength Title]**: [Explanation backed by cited evidence].

---

## 4. Deep-Dive Evidence Breakdown

### Section A: Financial & Business Viability
- **Entity Type & Funding**: [Public (Ticker) / Private (Series X, $YM raised)]
- **Revenue & Growth Metrics**: [Hard metrics, ARR, profit margins, or runway estimates]
- **Market Position & Vulnerabilities**: [Macro risks, customer reliance]
- **Sources Consulted**: [List of URLs with timestamps]

### Section B: Layoff History & Role Longevity
- **Historical Layoffs**: [Dates, % of workforce affected, reasons cited]
- **WARN Act Activity**: [Any state/provincial filings on record]
- **Turnover & Org Changes**: [Executive shifts, department reorg frequency]
- **Sources Consulted**: [List of URLs with timestamps]

### Section C: Daily Culture, WLB & Management
- **Expected Work Hours**: [Average weekly hours from Levels.fyi/community]
- **On-Call & Incident Burden**: [Frequency, compensation, rotation health]
- **Management Sentiment**: [Psychological safety, micro-management signals]
- **Sources Consulted**: [List of URLs with timestamps]

### Section D: Tech Stack & Engineering Architecture
- **Primary Stack**: [Languages, frameworks, cloud tooling]
- **Operational Complexity & Debt**: [Modern cloud-native vs. legacy maintenance vs. over-engineering]
- **Engineering Autonomy & DX**: [Release cycles, CI/CD health, QA practices]
- **Sources Consulted**: [List of URLs with timestamps]

---

## 5. Reverse-Interview Action Playbook

*Sharp, professional questions tailored to probe the exact risks and unverified flags uncovered in this audit during interviews.*

### For the Hiring Manager / Leadership:
1. **[Question targeting specific Yellow/Red flag]**: *"..."* (Intent: [What answer to look for])
2. **[Question targeting financial runway / roadmap priority]**: *"..."* (Intent: [What answer to look for])

### For Peer Engineers / Team Members:
1. **[Question targeting on-call reality and sprint pace]**: *"..."* (Intent: [What answer to look for])
2. **[Question targeting operational complexity and DX]**: *"..."* (Intent: [What answer to look for])
