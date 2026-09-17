---
name: candidate-employer-due-diligence
description: "Rigorous, multi-agent due diligence pipeline for candidate employers. Evaluates business stability, layoff risk, work-life balance, employee treatment, tech stack health, and role viability with zero-sugarcoating, adaptive multi-source triangulation, and reverse-interview generation."
user-invocable: true
---

# Candidate Employer Due Diligence Skill

A specialized, high-integrity research pipeline for career transitions. Designed to evaluate prospective employers objectively across business stability, employment longevity, work-life balance, engineering culture, and role risk before making career commitments.

---

## 1. Core Invariants & Anti-Hallucination Guardrails

To protect the candidate from catastrophic career moves (e.g., joining right before a layoff, entering an abusive on-call rotation, or inheriting crippling technical debt), this skill enforces four non-negotiable invariants:

### 1. The Zero-Sugarcoating Invariant (Brutal Honesty)
- Corporate PR, self-published marketing blogs, and recruiter pitches are treated as **unverified claims ($cf = 0.10$)**.
- The agent must **never euphemize red flags** (e.g., do not call "uncompensated 70-hour weeks" a "fast-paced entrepreneurial environment").
- When evidence points to high turnover, toxic management, or financial distress, report it explicitly as a **Critical Risk**.

### 2. Strict Decoupling of Employer Health vs. Candidate Alignment
- **The Health Invariant**: The **Objective Employer & Role Health Scorecard** measures *only* factual business stability, financial runway, historical layoff risk, operating friction, and leadership sanity.
- **No Keyword / Fit Inflation**: A candidate being a 100% technical match for a role **must NEVER inflate or mask** a company's financial instability, high turnover, or architectural dysfunction.
- **No Technology Glamour**: The presence of modern or trendy tech (e.g., NestJS, Kafka, AI APIs) is **not** an automatic indicator of engineering health. It must be evaluated for operational complexity, maintenance overhead, and over-engineering risk.
- **Dual-Index Output**: The audit produces two strictly non-overlapping indexes:
  1. *Index 1: Objective Employer & Role Health (Macro Stability)*
  2. *Index 2: Candidate Match & Interview Positioning (Personal Alignment)*

### 3. Anti-Hollow-Orchestration Invariant
- Sub-issues or subagents are **real units of decoupled execution**, not decorative checklists.
- **Prohibited**: Creating child sub-issues directly in `done` status without posted comments/evidence.
- Every research pillar must produce its own self-contained evidence payload in its dedicated ticket or subagent transcript before the parent synthesis begins.

### 4. The "Floor, Not Ceiling" Source Boundary
- The agent **must satisfy minimum baseline categories**, but is **never restricted to a fixed static list**.
- If a source dies, gets paywalled, or blocks automated access (e.g., Glassdoor/LinkedIn bot walls), the agent must dynamically discover alternative high-signal sources rather than failing or skipping the pillar.

---

## 2. Orchestration Protocols

Depending on the runtime environment, the agent must strictly follow the corresponding orchestration workflow:

### Mode A: Ticket / Issue-Tracking Environment (e.g., Multica Platform)
When the audit is triggered on a parent issue in Multica:

```
[Parent Ticket: Audit Employer] (Status: in_progress)
   │
   ├── Phase 1 (Fan-Out): Create 4 Child Tickets in 'todo' status
   │      ├── Child 1: "Track 1: Financial & Business Health"
   │      ├── Child 2: "Track 2: Layoff & Stability History"
   │      ├── Child 3: "Track 3: Culture, WLB & Management Quality"
   │      └── Child 4: "Track 4: Role Scope, Tech Stack & Architecture"
   │
   ├── Phase 2 (Pillar Execution & Child Comments):
   │      ├── Run Track 1 research → Post full findings to Child 1 comment → Set Child 1 to 'done'
   │      ├── Run Track 2 research → Post full findings to Child 2 comment → Set Child 2 to 'done'
   │      ├── Run Track 3 research → Post full findings to Child 3 comment → Set Child 3 to 'done'
   │      └── Run Track 4 research → Post full findings to Child 4 comment → Set Child 4 to 'done'
   │
   └── Phase 3 (Fan-In & Synthesis):
          └── Read comments from Children 1-4 → Synthesize Master Dossier on Parent Ticket → Set Parent to 'done' / 'in_review'
```

#### Exact Multica CLI Sequence:
1. **Scaffold Sub-Issues in `todo`**:
   ```bash
   multica issue create --title "Track 1: Financial & Business Health" --parent <parent-id> --project <project-id> --status todo
   multica issue create --title "Track 2: Layoff & Stability History" --parent <parent-id> --project <project-id> --status todo
   multica issue create --title "Track 3: Culture, WLB & Management Quality" --parent <parent-id> --project <project-id> --status todo
   multica issue create --title "Track 4: Role Scope, Tech Stack & Architecture" --parent <parent-id> --project <project-id> --status todo
   ```
2. **Execute and Post to Each Child**:
   * For each child issue, execute the dedicated search, write findings to `./trackN_findings.md`, and run:
     ```bash
     multica issue comment add <child-id> --content-file "./trackN_findings.md"
     multica issue status <child-id> done --no-start
     ```
3. **Synthesize on Parent**:
   * Ingest all 4 child comments, generate the unified Due Diligence Dossier, write to `./final_dossier.md`, and run:
     ```bash
     multica issue comment add <parent-id> --content-file "./final_dossier.md"
     ```

---

### Mode B: Standalone / Subagent Environment (Chat or CLI without Ticket Tracking)
When running in a direct chat room or an autonomous runtime without parent issue tracking:

```
[Lead Synthesizer Agent]
   │
   ├── Step 1: Dispatch 4 Parallel Subagents (invoke_subagent)
   │      ├── Subagent 1: Role 'Financial Auditor' (Pillar 1 prompt)
   │      ├── Subagent 2: Role 'Layoff & Stability Auditor' (Pillar 2 prompt)
   │      ├── Subagent 3: Role 'Culture & WLB Auditor' (Pillar 3 prompt)
   │      └── Subagent 4: Role 'Architecture & Tech Auditor' (Pillar 4 prompt)
   │
   ├── Step 2: Await Structured Subagent Deliverables (isolated context)
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

All research outputs must follow this standardized Markdown schema:

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
