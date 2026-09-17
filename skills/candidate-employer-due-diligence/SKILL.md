---
name: candidate-employer-due-diligence
description: "Rigorous, multi-agent due diligence pipeline for candidate employers. Evaluates business stability, layoff risk, work-life balance, employee treatment, tech stack health, and role viability with zero-sugarcoating, adaptive multi-source triangulation, and reverse-interview generation."
user-invocable: true
---

# Candidate Employer Due Diligence Skill

A specialized, high-integrity research pipeline for career transitions. Designed to evaluate prospective employers objectively across business stability, employment longevity, work-life balance, engineering culture, and role risk before making career commitments.

---

## 1. Core Principles & Guardrails

To protect the candidate from catastrophic career moves (e.g., joining right before a layoff, entering an abusive on-call rotation, or inheriting crippling technical debt), this skill enforces three non-negotiable invariants:

### 1. The Zero-Sugarcoating Invariant (Brutal Honesty)
- Corporate PR, self-published marketing blogs, and recruiter pitches are treated as **unverified claims ($cf = 0.10$)**.
- The agent must **never euphemize red flags** (e.g., do not call "uncompensated 70-hour weeks" a "fast-paced entrepreneurial environment").
- When evidence points to high turnover, toxic management, or financial distress, report it explicitly as a **Critical Risk**.

### 2. The Context-Decoupled "Divide & Conquer" Architecture
- **Problem**: Running deep web searches, document scraping, and forum analysis for 4+ research pillars inside a single session quickly saturates LLM context windows, causing hallucinations, dropped details, and superficial summaries.
- **Solution**: The primary agent **must delegate** research to specialized sub-tracks or subagents for each pillar. Each worker collects raw data and produces a structured sub-report. The lead agent only ingests the sub-reports for final synthesis.

### 3. The "Floor, Not Ceiling" Source Boundary
- The agent **must satisfy minimum baseline categories**, but is **never restricted to a fixed static list**.
- If a source dies, gets paywalled, or blocks automated access (e.g., Glassdoor/LinkedIn bot walls), the agent must dynamically discover alternative high-signal sources rather than failing or skipping the pillar.

---

## 2. Multi-Agent Pipeline Topology

```
                  [ Master Due Diligence Ticket / Lead Agent ]
                                       │
         ┌──────────────────┬──────────┴──────────┬──────────────────┐
         ▼                  ▼                     ▼                  ▼
    [ Worker 1 ]       [ Worker 2 ]          [ Worker 3 ]       [ Worker 4 ]
   Financial & Biz    Layoff & Stability    Culture, WLB &    Role & Tech Stack
     Health Track        History Track       Employee Exp           Track
         │                  │                     │                  │
         └──────────────────┼─────────────────────┼──────────────────┘
                            ▼
        [ Lead Synthesizer: Quality Gate & Dossier Assembly ]
                            │
                            ├── 1. Executive TL;DR & Scorecard (Grades A–F)
                            ├── 2. Verified Red & Yellow Flag Matrix
                            ├── 3. Deep-Dive Evidence Chapters
                            └── 4. Tailored Reverse-Interview Playbook
```

---

## 3. The 4 Specialized Research Pillars & Minimum Baselines

Every employer audit must cover these 4 pillars. Each worker must query at least the baseline channels and dynamically follow high-signal leads.

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
*Goal: Evaluate technical debt, engineering autonomy, tooling friction, and career growth potential.*

* **Minimum Baseline Inquiries:**
  * **Tech Stack Modernity**: Core technologies, cloud infrastructure, CI/CD pipeline maturity, automated testing coverage.
  * **Engineering Footprint**: Public GitHub organization activity, engineering blogs, tech conference talks, open-source contributions.
  * **Role Danger Signals**: Vague job responsibilities ("wear many hats" disguised as doing 3 roles), legacy system firefighting, or obsolete legacy frameworks (e.g. unmaintained bespoke monoliths).

---

## 4. Standardized Output Schema: Employer Due Diligence Dossier

All research outputs must follow this standardized Markdown schema to ensure consistency, comparability between employers, and actionable decision-making.

```markdown
# Employer Due Diligence Dossier: [Company Name]
**Target Role / Team:** [Role Title, if known]  
**Audit Date:** [YYYY-MM-DD]  
**Overall Verdict:** [🟢 HIGH CONFIDENCE FIT / 🟡 PROCEED WITH CAUTION / 🔴 SIGNIFICANT RISK]  
**Confidence Rating:** [High (80-100%) / Medium (50-79%) / Low (<50%)]

---

## 1. Executive Summary & Decision Scorecard

| Dimension | Grade (A–F) | Key Signal | Risk Level |
| :--- | :---: | :--- | :---: |
| **1. Financial Stability & Runway** | [A/B/C/D/F] | [1-line summary] | [Low / Med / High] |
| **2. Role & Org Stability (Layoff Risk)** | [A/B/C/D/F] | [1-line summary] | [Low / Med / High] |
| **3. Work-Life Balance & Culture** | [A/B/C/D/F] | [1-line summary] | [Low / Med / High] |
| **4. Tech Stack & Engineering Health** | [A/B/C/D/F] | [1-line summary] | [Low / Med / High] |
| **5. Compensation & Career Growth** | [A/B/C/D/F] | [1-line summary] | [Low / Med / High] |

### TL;DR Verdict
[3–4 concise sentences outlining the bottom-line truth: Is this a stable, high-growth environment, a high-burn grindhouse, or a volatile turnaround? Clear recommendation on whether to pursue, negotiate with conditions, or decline.]

---

## 2. Risk & Flag Matrix

### 🔴 Critical Red Flags (Dealbreakers)
- **[Flag Title]**: [Explanation backed by cited evidence].

### 🟡 Yellow Flags (Require Direct Verification)
- **[Flag Title]**: [Explanation backed by cited evidence].

### 🟢 Positive Strengths (Selling Points)
- **[Strength Title]**: [Explanation backed by cited evidence].

---

## 3. Deep-Dive Evidence Breakdown

### Section A: Financial & Business Viability
- **Entity Type & Funding**: [Public (Ticker) / Private (Series X, $YM raised)]
- **Revenue & Growth Metrics**: [Trends, profit margins, or runway estimates]
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
- **Technical Debt & Legacy Load**: [Modern cloud-native vs. legacy maintenance]
- **Engineering Autonomy**: [Release cycles, CI/CD health, QA practices]
- **Sources Consulted**: [List of URLs with timestamps]

---

## 4. Reverse-Interview Action Playbook

*Sharp, professional questions tailored to probe the exact risks and blind spots uncovered in this audit during interviews.*

### For the Hiring Manager:
1. **[Question 1 targeting specific Yellow/Red flag]**: *"..."* (Intent: [What answer to look for])
2. **[Question 2 targeting team stability / roadmap]**: *"..."* (Intent: [What answer to look for])

### For Peer Engineers / Team Members:
1. **[Question 1 targeting on-call reality and sprint pace]**: *"..."* (Intent: [What answer to look for])
2. **[Question 2 targeting tech debt and release friction]**: *"..."* (Intent: [What answer to look for])
```

---

## 5. Step-by-Step Execution Protocol for Agents

When requested to audit a candidate employer:

1. **Step 1 — Initialize & Scaffold**:
   - Check if the target is a public or private company, target role, and location.
2. **Step 2 — Dispatch Specialized Workers (Divide & Conquer)**:
   - Worker 1 executes Financial & Business Health queries.
   - Worker 2 executes Layoff History, WARN records & Org Stability queries.
   - Worker 3 executes Culture, WLB, Levels.fyi & Community Discourse queries.
   - Worker 4 executes Tech Stack, GitHub footprint & Engineering Culture queries.
3. **Step 3 — Triangulate & Detect Conflicting Claims**:
   - Resolve discrepancies between official company claims and employee/market data.
   - Assign a **Confidence Score** based on source credibility and freshness.
4. **Step 4 — Generate Dossier & Reverse-Interview Playbook**:
   - Compile into the standardized Markdown template.
   - Formulate pointed questions to resolve unverified yellow flags during the candidate's actual interview.
