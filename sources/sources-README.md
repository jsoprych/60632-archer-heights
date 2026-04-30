# Authoritative Benchmark & Pricing Sources

## The Big 4 (Bookmark These)

### 1. Artificial Analysis (artificialanalysis.ai)
- **What:** Best single source. Intelligence Index v4.0 composite of 10 benchmarks (GDPval-AA, GPQA Diamond, Terminal-Bench Hard, SciCode, AA-LCR, AA-Omniscience, IFBench, HLE, CritPt). Tests every model on identical hardware.
- **Why trust it:** Independent. Tests every model in-house. Not vendor-reported. Updated within days of each release.
- **Covers:** 347 models ranked. Intelligence Index + pricing + speed + latency + context window per model.
- **URL:** https://artificialanalysis.ai/leaderboards/models

### 2. Vals AI (vals.ai)
- **What:** Independent multi-benchmark evaluation suite. Their own Vals Index composite, plus individual benchmarks (SWE-bench, Terminal-Bench, Corp Fin, Case Law, Vibe Code).
- **Why trust it:** Independent testing (not vendor-reported). Has both "Vals Index" composite and per-benchmark drill-downs. Proprietary non-public datasets prevent contamination.
- **Covers:** 46 models tested. Finance, law, coding, education benchmarks.
- **URL:** https://www.vals.ai/benchmarks

### 3. LM Arena (lmarena.ai)
- **What:** Crowd-sourced blind pairwise comparisons. 6M+ human votes → Elo ratings. The gold standard for "which model do real users prefer."
- **Why trust it:** 6M+ blind votes from real users. Most widely referenced human preference benchmark. Models can't game it by optimizing for specific test answers.
- **Covers:** All major models ranked by human preference Elo.
- **URL:** https://lmarena.ai

### 4. PricePerToken (pricepertoken.com)
- **What:** Single-page comparison of pricing + benchmark scores per model. Interactive chart: X-axis benchmarks (MMLU-Pro, GPQA, Math Hard, LiveCodeBench, AIME), Y-axis pricing.
- **Why trust it:** Aggregates pricing from official API docs + benchmark scores from original leaderboards. Good for "score vs cost" at a glance.
- **Covers:** All major providers, pricing per 1M tokens + per-benchmark scores.
- **URL:** https://pricepertoken.com

## Secondary Tier (Cross-Reference)

### 5. BenchLM.ai
- **What:** Model profile pages with 20+ benchmark scores each. Provisional and verified leaderboards.
- **Why trust it:** Good for deep-diving a single model across many benchmarks.
- **URL:** https://benchlm.ai

### 6. BuildFastWithAI
- **What:** Monthly AI model roundups with curated benchmark tables and cost analysis.
- **Why trust it:** Journalist-quality curation. Links back to original sources (vals.ai, AA, official reports). Good for narrative context.
- **URL:** https://www.buildfastwithai.com/blogs/best-ai-models-leaderboard-april-2026-updated

### 7. Ofox.ai
- **What:** Aggregated model comparison with pricing, benchmarks, and availability guides.
- **Why trust it:** Links every number to its original leaderboard source. Good editorial standards.
- **URL:** https://ofox.ai/blog/llm-leaderboard-best-ai-models-ranked-2026/

### 8. HF Spaces (Hugging Face)
- **What:** Official leaderboard spaces maintained by benchmark creators (GAIA, SWE-bench, LM Arena, Artificial Analysis).
- **Why trust it:** Primary source — run by the benchmark creators themselves.
- **URLs:**
  - https://huggingface.co/spaces/lmarena-ai/arena-leaderboard
  - https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard
  - https://huggingface.co/spaces/gaia-benchmark/leaderboard

### 9. Official API Docs (Primary Source for Pricing)
- **DeepSeek:** https://api-docs.deepseek.com/quick_start/pricing
- **OpenAI:** https://openai.com/api/pricing/
- **Anthropic:** https://anthropic.com/pricing

### 10. VentureBeat / TechCrunch
- **What:** Third-party reporting with direct access to model vendors. Good for launch-day benchmark confirmations.
- **Example:** VentureBeat's DeepSeek V4 article cross-referenced vendor tables with independent analysis.

## Data Refresh Cadence
- Artificial Analysis: Updated within 1-3 days of each model release
- Vals AI: Updated within 1-2 weeks of each model release
- LM Arena: Continuous (new models added via blind battles)
- PricePerToken: Updated weekly
- Recommended: Pull from AA + Vals + LM Arena weekly, cross-reference with PricePerToken
