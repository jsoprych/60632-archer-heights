# AI Benchmark & Pricing Intelligence — Authoritative Sources
## Hermes Agent — April 30, 2026

This is the master reference for all benchmark data. Every score in our charts
must trace back to one of these sources. No second-hand data.

## BENCHMARK LEADERBOARDS (Official/Authoritative)

### 1. LM Arena (formerly LMSYS Chatbot Arena)
  URL: https://lmarena.ai/ (also arena.ai/leaderboard)
  HF Space: https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard
  What: Human preference rankings via blind A/B voting
  Scale: 5.8M+ votes, 339+ models
  Maintainer: UC Berkeley → Arena Intelligence
  Updates: Continuous (live)
  Apr 2026 leader: Claude Opus 4.7 at 1504 Elo

### 2. SWE-bench Verified (Official)
  URL: https://www.swebench.com/verified.html
  Independent: https://www.vals.ai/benchmarks/swebench
  What: Real GitHub issue resolution (500 Python tasks)
  Maintainer: Princeton University (original), OpenAI (Verified subset)
  Apr 2026 leader: Claude Mythos Preview at 93.9%

### 3. Artificial Analysis Intelligence Index
  URL: https://artificialanalysis.ai/leaderboards/models
  What: Composite intelligence index across 10+ evals
  Maintainer: Artificial Analysis
  Apr 2026 leader: GPT-5.5 (xhigh) at 60

### 4. Vals AI Index
  URL: https://www.vals.ai/home
  What: Independent multi-benchmark evaluation
  Maintainer: Vals AI
  Updates: Continuous

### 5. Price Per Token Benchmark
  URL: https://pricepertoken.com/leaderboards/benchmark
  What: MMLU, MMLU-Pro, GPQA, GAIA, AIME, HumanEval scores + pricing
  Maintainer: 68 Ventures, LLC

### 6. BenchLM.ai
  URL: https://benchlm.ai/
  What: Weighted composite scoring across benchmarks
  Maintainer: BenchLM

### 7. GAIA (Official Leaderboard)
  URL: https://hal.cs.princeton.edu/gaia
  HF Space: https://huggingface.co/spaces/gaia-benchmark/leaderboard
  What: General AI Assistants — multi-step reasoning + tool use
  Maintainer: Meta AI / Princeton
  Apr 2026 leader: Claude Mythos Preview at 52.3%

### 8. Open LLM Leaderboard (HuggingFace)
  URL: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
  What: Open-weight model benchmarks
  Maintainer: HuggingFace

### 9. LiveBench
  URL: https://livebench.ai/
  What: Contamination-free benchmark (new questions)
  Maintainer: LiveBench team

### 10. MMLU-Pro Official
  URL: https://pricepertoken.com/leaderboards/benchmark/mmlu-pro
  Apr 2026 leader: Gemini 3 Pro Preview at 89.8%

### 11. GPQA Diamond
  URL: https://pricepertoken.com/leaderboards/benchmark/gpqa
  Apr 2026 leader: Gemini 3.1 Pro Preview at 94.1%

### 12. Onyx AI LLM Leaderboard
  URL: https://onyx.app/llm-leaderboard
  What: Multi-benchmark comparison across all major models

### 13. Klü LLM Leaderboard
  URL: https://klu.ai/llm-leaderboard
  What: Multi-benchmark including GAIA, GPQA, MMMU

### 14. Scale AI Leaderboard
  URL: https://labs.scale.com/leaderboard
  What: Expert-driven benchmarks including SWE-bench Pro

### 15. buildfastwithai.com
  URL: https://www.buildfastwithai.com/blogs/best-ai-models-april-2026
  URL: https://www.buildfastwithai.com/blogs/best-ai-models-leaderboard-april-2026-updated
  What: Monthly comprehensive analysis with scores from multiple sources
  Note: Secondary aggregator, useful for cross-referencing

## MODEL SCORE SOURCES (Direct)

- OpenAI: https://developers.openai.com/api/docs/guides/evals
- Anthropic: https://docs.anthropic.com/en/docs/about-claude/models
- Google DeepMind: https://ai.google.dev/ 
- Meta AI: https://llama.meta.com/
- DeepSeek: https://api-docs.deepseek.com/
- Alibaba Qwen: https://qwen.readthedocs.io/
- Mistral AI: https://docs.mistral.ai/
- xAI/Grok: https://docs.x.ai/
- Z.ai (GLM): https://z.ai/

## PRICING SOURCES

- https://artificialanalysis.ai/leaderboards/models (price + intelligence)
- https://pricepertoken.com/ (benchmark-specific pricing)
- https://ofox.ai/en/models (aggregated pricing)

## METHODOLOGY NOTES

1. SWE-bench Verified has contamination concerns — many training datasets include
   GitHub content. OpenAI stopped reporting Verified scores in early 2026.
   SWE-bench Pro is the harder, uncontaminated successor (by Scale AI).

2. MMLU is largely saturated — frontier models all score 85%+. MMLU-Pro is now
   the preferred variant for differentiation.

3. GAIA scores are low (best is ~52%) because it requires real tool use and
   multi-step reasoning, not pattern matching.

4. LM Arena scores are human preference, not capability — a higher Elo means
   people prefer the responses, not necessarily that the model is "smarter."

5. Artificial Analysis Intelligence Index is a composite — it aggregates 10+
   evals into a single score. Useful for overall positioning.

6. Always prefer third-party verified scores (vals.ai, Artificial Analysis)
   over vendor self-reports. Mark vendor-reported with ★.

## RECOMMENDED BENCHMARKS FOR OUR CHARTS

For a balanced view of model capability, track these 5:
  A. LM Arena Elo — human preference (practical quality)
  B. SWE-bench Verified — coding (most cited)
  C. GPQA Diamond — science reasoning (hardest reasoning)
  D. MMLU-Pro — general knowledge (replaces saturated MMLU)
  E. GAIA — agent/tool use (most relevant to what we do)
  F. Price per 1M input tokens — cost comparison
