# AI Model Benchmark & Pricing Intelligence
## Master Data Schema — Hermes Agent Research Program

This is a living reference. Every benchmark, every model score, every price point
has source URLs attached. Updated daily by the 2PM UTC cron.

## Benchmarks We Track

| ID | Name | What It Measures | Creator | Year |
|-----|------|-----------------|---------|------|
| mmlu | MMLU | Multi-task knowledge (57 subjects) | UC Berkeley | 2020 |
| mmlu-pro | MMLU-Pro | Harder MMLU, more reasoning | MBZUAI | 2024 |
| humaneval | HumanEval | Code generation (Python) | OpenAI | 2021 |
| math | MATH | Math word problems | OpenAI | 2021 |
| math-500 | MATH-500 | Subset of MATH | OpenAI | 2024 |
| gpqa | GPQA | Graduate-level science reasoning | NYU/Anthropic | 2023 |
| gpqa-diamond | GPQA Diamond | Hardest GPQA subset | NYU/Anthropic | 2023 |
| swe-bench | SWE-bench | Software engineering (real GitHub issues) | Princeton | 2023 |
| swe-bench-v | SWE-bench Verified | Verified subset of SWE-bench | Princeton | 2024 |
| arena-elo | Chatbot Arena ELO | Human preference rankings | LMSYS | 2023 |
| hellaswag | HellaSwag | Commonsense reasoning | UW/AI2 | 2019 |
| truthfulqa | TruthfulQA | Truthfulness/factuality | OpenAI/Anthropic | 2021 |
| gaia | GAIA | General AI Assistants (tool use) | Meta/Princeton | 2023 |
| simpleqa | SimpleQA | Short factuality questions | OpenAI | 2024 |
| livebench | LiveBench | Contamination-free (new questions) | LiveBench team | 2024 |
| aime | AIME | American Invitational Math Exam | MAA | 2024 |
| bigbench | BIG-Bench Hard | Challenging reasoning | Google | 2022 |
| frontier-math | FrontierMath | Advanced math research | Epoch AI | 2024 |

## Models We Track

US Frontier: GPT-4o, GPT-4o-mini, o1, o3-mini, GPT-4.5, Claude 3.5 Sonnet, Claude Opus 4, Gemini 2.0 Flash, Gemini 2.5 Pro, Grok 2, Grok 3, Llama 3.1 405B, Llama 4
Chinese Frontier: DeepSeek-V3, DeepSeek-R1, DeepSeek-V4, Qwen2.5-72B, Qwen3, GLM-5, Kimi K2
Small (<20B): Phi-4, Llama 3.2 3B/8B, Qwen2.5-7B, DeepSeek-R1-Distills, Mistral 7B, Gemma 2

## Sources We Use (verified, independent)

1. pricepertoken.com — pricing + GAIA/MMLU/GPQA scores
2. onyx.app/llm-leaderboard — multi-benchmark comparison
3. artificialanalysis.ai — intelligence index + pricing
4. vellum.ai/llm-leaderboard — benchmark scores
5. benchlm.ai — scored aggregation
6. klu.ai/llm-leaderboard — multi-benchmark
7. hal.cs.princeton.edu/gaia — official GAIA leaderboard
8. livebench.ai — contamination-free benchmark
9. huggingface.co/spaces/gaia-benchmark/leaderboard — official GAIA HF space
10. openwebui.com/leaderboard — real usage data
11. llm-stats.com — pricing + benchmarks
12. buildfastwithai.com — monthly analysis with scores
13. ofox.ai — LLM leaderboard
14. lmarena.ai — official Chatbot Arena
15. github.com/openai/simple-evals — OpenAI eval suite
