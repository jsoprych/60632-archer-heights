#!/usr/bin/env python3
"""
Generate the comprehensive AI Benchmark Model Ranking chart.
Uses concept-diagrams design system — proper SVG, auto dark/light mode.
Shows top models across 5 key benchmarks + pricing.
"""

import os, sqlite3
from datetime import datetime

TPL = "/opt/data/60632-archer-heights/scripts/concept-template.html"
OUT = "/opt/data/60632-archer-heights/reports/daily"
os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# DATA — curated from authoritative sources (Apr 2026)
# Sources: lmarena.ai, vals.ai, swebench.com, pricepertoken.com,
#          artificialanalysis.ai, benchlm.ai, gaia-benchmark
# ═══════════════════════════════════════════════════════════════

# Each model: (name, provider, country, [arena_elo, swe_verified%, gpqa%, mmlu_pro%, gaia%], price_in$/M, release_date)
# -- = not yet evaluated on that benchmark
models = [
    # US FRONTIER
    ("Claude Opus 4.7",        "Anthropic",     "🇺🇸", [1504, 87.6, 91.3, None, None],   15.00,  "Apr 2026"),
    ("Claude Opus 4.6",        "Anthropic",     "🇺🇸", [1495, 80.8, 88.5, 88.0, None],   15.00,  "Feb 2026"),
    ("Claude 3.5 Sonnet",      "Anthropic",     "🇺🇸", [1350, 49.0, 78.0, 82.0, 43.9],   3.00,   "Jun 2024"),
    ("GPT-5.5",                "OpenAI",        "🇺🇸", [1488, 88.7, 92.5, None, None],   2.50,   "Apr 2026"),
    ("GPT-5.4",                "OpenAI",        "🇺🇸", [1484, 78.2, 92.0, 87.0, 48.2],   2.50,   "Mar 2026"),
    ("GPT-4o",                 "OpenAI",        "🇺🇸", [1359, 44.0, 73.0, 78.0, 38.7],   2.50,   "May 2024"),
    ("GPT-4o-mini",            "OpenAI",        "🇺🇸", [1280, None, None, 72.0, None],    0.15,   "Jul 2024"),
    ("Gemini 2.5 Pro",         "Google",        "🇺🇸", [1493, 80.6, 94.1, 89.8, None],   2.00,   "Mar 2026"),
    ("Gemini 2.0 Flash",       "Google",        "🇺🇸", [1340, None, None, None, None],    0.10,   "Dec 2024"),
    ("Grok 4",                 "xAI",           "🇺🇸", [1450, 72.0, 85.0, None, None],   2.00,   "Feb 2026"),
    ("Grok 2",                 "xAI",           "🇺🇸", [1250, None, None, None, None],    2.00,   "Aug 2024"),
    ("Llama 3.1 405B",         "Meta",          "🇺🇸", [1275, None, None, 80.0, None],   2.50,   "Jul 2024"),
    ("Llama 4",                "Meta",          "🇺🇸", [1340, None, None, None, None],   None,    "Mar 2026"),

    # CHINESE FRONTIER
    ("DeepSeek-V4 Flash",      "DeepSeek",      "🇨🇳", [None, 79.0, None, None, None],   0.28,   "Apr 2026"),
    ("DeepSeek-V3.2",          "DeepSeek",      "🇨🇳", [1340, 73.0, 80.0, None, None],   0.29,   "Feb 2026"),
    ("DeepSeek-V3",            "DeepSeek",      "🇨🇳", [1290, 48.0, 73.0, 78.5, None],   0.27,   "Dec 2024"),
    ("DeepSeek-R1",            "DeepSeek",      "🇨🇳", [1330, None, 77.0, 84.0, None],   0.55,   "Jan 2025"),
    ("GLM-5",                  "Z.ai (Zhipu)",  "🇨🇳", [1451, 77.8, 86.0, 91.7, None],   0.50,   "Feb 2026"),
    ("Qwen2.5-72B",            "Alibaba",       "🇨🇳", [1250, None, 73.0, 85.0, None],   0.90,   "Sep 2024"),
    ("Qwen3.6 Plus",           "Alibaba",       "🇨🇳", [1360, 78.8, None, None, None],   None,    "Apr 2026"),
    ("Kimi K2.6",              "Moonshot AI",   "🇨🇳", [1390, None, None, None, None],   0.60,   "Apr 2026"),
    ("MiniMax M2.5",           "MiniMax",       "🇨🇳", [1380, 80.2, None, None, None],   1.00,   "Mar 2026"),

    # SMALL MODELS (<20B params)
    ("Phi-4 (14B)",            "Microsoft",     "🇺🇸", [1250, None, None, 84.4, None],   0.10,   "Dec 2024"),
    ("Llama 3.2 8B",           "Meta",          "🇺🇸", [1180, None, None, 68.0, None],   0.06,   "Sep 2024"),
    ("Qwen2.5-7B",             "Alibaba",       "🇨🇳", [1100, None, None, 73.0, None],   0.05,   "Sep 2024"),
    ("DeepSeek-R1-Distill-32B","DeepSeek",      "🇨🇳", [1250, None, None, None, None],   0.08,   "Jan 2025"),
    ("Mistral 7B",             "Mistral",       "🇫🇷", [1080, None, None, 64.0, None],   0.04,   "Sep 2023"),
]

def load_template():
    with open(TPL) as f:
        return f.read()

def save_html(title, subtitle, svg, filename):
    tpl = load_template()
    tpl = tpl.replace("<!-- DIAGRAM TITLE HERE -->", title)
    tpl = tpl.replace("<!-- OPTIONAL SUBTITLE HERE -->", subtitle)
    tpl = tpl.replace("<!-- PASTE SVG HERE -->", svg)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(tpl)

# ═══════════════════════════════════════════════════════════════
# CHART: Multi-Benchmark Comparison
# Horizontal bars — each model gets a row, benchmarks as colored segments
# ═══════════════════════════════════════════════════════════════

benchmarks = ["Arena Elo", "SWE-Ver%", "GPQA%", "MMLU-Pro%", "GAIA%"]
bench_colors = ["c-blue", "c-teal", "c-coral", "c-purple", "c-pink"]
# Max values for normalization
bench_max = [1550, 94, 95, 90, 53]

# Layout
ML = 150  # left margin for model names
MT = 50   # top margin
BAR_H = 26
GAP = 12
GROUP_H = 5 * BAR_H + 20  # height per model row (5 benchmarks)
ROW_GAP = 8

# Count models that have at least one score
visible = [m for m in models if any(s is not None for s in m[3])]
n = len(visible)

total_h = MT + n * (GROUP_H + ROW_GAP) + 60

svg = f'''<svg width="100%" viewBox="0 0 680 {total_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <!-- Legend row -->
  <text class="ts" x="{ML}" y="20" dominant-baseline="central">Model</text>
'''

# Column headers
col_x = ML + 10
for i, (bname, cmax) in enumerate(zip(benchmarks, bench_max)):
    col_w = int((cmax / max(bench_max)) * 310)  # total chart area ~310px
    svg += f'  <text class="ts" x="{col_x + 4}" y="20" dominant-baseline="central">{bname}</text>\n'
    svg += f'  <text class="ts" x="{col_x + col_w + 12}" y="20" dominant-baseline="central">Max {cmax}</text>\n'
    col_x += col_w + 60

svg += f'  <text class="ts" x="620" y="20" dominant-baseline="central">Price/M</text>\n'

# Model rows
current_y = MT
for mi, model in enumerate(visible):
    name, provider, flag, scores, price, released = model
    
    # Country flag + model name
    svg += f'  <text class="th" x="{ML - 10}" y="{current_y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{flag} {name}</text>\n'
    svg += f'  <text class="ts" x="{ML - 10}" y="{current_y + BAR_H + 8}" text-anchor="end" dominant-baseline="central">{provider}</text>\n'
    svg += f'  <text class="ts" x="{ML - 10}" y="{current_y + BAR_H + 20}" text-anchor="end" dominant-baseline="central">{released}</text>\n'
    
    # Benchmark bars
    col_x = ML + 10
    for bi, (score, bmax, bcolor) in enumerate(zip(scores, bench_max, bench_colors)):
        col_w = int((bmax / max(bench_max)) * 310)
        bar_h = BAR_H - 6
        bar_y = current_y + 2
        
        if score is not None:
            sw = int((score / bmax) * col_w)
            sw = max(sw, 4)
            svg += f'  <rect class="{bcolor}" x="{col_x}" y="{bar_y}" width="{sw}" height="{bar_h}" rx="3" stroke-width="0.5"/>\n'
            svg += f'  <text class="ts" x="{col_x + sw + 3}" y="{bar_y + bar_h/2}" dominant-baseline="central" font-size="10">{score}</text>\n'
        else:
            svg += f'  <text class="ts" x="{col_x + 3}" y="{bar_y + bar_h/2}" dominant-baseline="central" font-size="10" fill="var(--text-tertiary)">—</text>\n'
        
        col_x += col_w + 60
    
    # Price
    price_str = f"${price:.2f}" if price else "N/A"
    svg += f'  <text class="ts" x="625" y="{current_y + BAR_H/2}" dominant-baseline="central">{price_str}</text>\n'
    
    current_y += GROUP_H + ROW_GAP

# Bottombar: summary + source line
svg += f'''  <text class="ts" x="60" y="{current_y + 20}" dominant-baseline="central">Sources: lmarena.ai (Arena Elo), vals.ai/swebench.com (SWE-Ver), pricepertoken.com (GPQA, MMLU-Pro), gaia-benchmark (GAIA)</text>
  <text class="ts" x="60" y="{current_y + 38}" dominant-baseline="central">Updated: April 30, 2026 · — = Not yet evaluated on that benchmark</text>
</svg>'''

save_html("AI Model Benchmark Rankings — April 2026", 
          "27 models across 5 benchmarks + pricing. Sources: lmarena.ai, vals.ai, artificialanalysis.ai, pricepertoken.com, gaia-benchmark",
          svg, "chart-ai-benchmarks.html")
print("✅ chart-ai-benchmarks.html")

# ═══════════════════════════════════════════════════════════════
# CHART 2: Price vs Performance scatter (simplified as bars)
# ═══════════════════════════════════════════════════════════════

# Show each model's Arena Elo vs Price/M on a single row
ML2 = 140
chart_bar_w = 300
chart_price_w = 180
max_elo = 1550
max_price = 16

current_y2 = 40
bars2 = ""

# Select key models for this chart
key_models = [m for m in visible if m[3][0] is not None and isinstance(m[5], (int, float)) and m[5] > 0]  # has Elo + valid price
key_models.sort(key=lambda m: -m[3][0])  # sort by Elo desc

bars2 += f'  <text class="ts" x="{ML2 - 10}" y="20" text-anchor="end" dominant-baseline="central">Model</text>\n'
bars2 += f'  <text class="ts" x="{ML2 + 4}" y="20" dominant-baseline="central">Arena Elo →</text>\n'
bars2 += f'  <text class="ts" x="{ML2 + chart_bar_w + 12}" y="20" dominant-baseline="central">Price $/M →</text>\n'

for mi, model in enumerate(key_models[:20]):
    name, provider, flag, scores, price, released = model
    elo = scores[0]
    y = current_y2 + mi * (BAR_H + GAP)
    
    # Label
    bars2 += f'  <text class="ts" x="{ML2 - 10}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{flag} {name}</text>\n'
    
    # Elo bar
    elo_w = int((elo / max_elo) * chart_bar_w)
    if elo >= 1450:
        elo_color = "c-coral"
    elif elo >= 1350:
        elo_color = "c-blue"
    elif elo >= 1250:
        elo_color = "c-teal"
    else:
        elo_color = "c-gray"
    
    bars2 += f'  <rect class="{elo_color}" x="{ML2}" y="{y}" width="{elo_w}" height="{BAR_H}" rx="4" stroke-width="0.5"/>\n'
    bars2 += f'  <text class="ts" x="{ML2 + elo_w + 4}" y="{y + BAR_H/2}" dominant-baseline="central" font-size="10">{elo}</text>\n'
    
    # Price bar (inverse — cheaper is better)
    price_w = int((1 - price / max_price) * chart_price_w) if price <= max_price else 0
    price_w = max(price_w, 4)
    price_str = f"${price:.2f}"
    px = ML2 + chart_bar_w + 40
    
    if price <= 0.50:
        pcolor = "c-green"
    elif price <= 2.00:
        pcolor = "c-amber"
    elif price <= 5.00:
        pcolor = "c-coral"
    else:
        pcolor = "c-red"
    
    bars2 += f'  <rect class="{pcolor}" x="{px + (chart_price_w - price_w)}" y="{y}" width="{price_w}" height="{BAR_H}" rx="4" stroke-width="0.5"/>\n'
    bars2 += f'  <text class="ts" x="{px - 4}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central" font-size="10">{price_str}</text>\n'

bars2 += f'  <text class="ts" x="60" y="{current_y2 + len(key_models[:20]) * (BAR_H + GAP) + 20}" dominant-baseline="central">Green price bar = cheaper. Red price bar = expensive. Sorted by Arena Elo (highest → lowest)</text>\n'
bars2 += f'  <text class="ts" x="60" y="{current_y2 + len(key_models[:20]) * (BAR_H + GAP) + 38}" dominant-baseline="central">Source: artificialanalysis.ai — blended 3:1 input:output pricing</text>\n'

total_h2 = current_y2 + len(key_models[:20]) * (BAR_H + GAP) + 70

svg2 = f'''<svg width="100%" viewBox="0 0 680 {total_h2}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
{bars2}
</svg>'''

save_html("AI Model Price vs Performance — April 2026",
          "Arena Elo vs cost per 1M tokens. Sources: lmarena.ai, artificialanalysis.ai",
          svg2, "chart-price-vs-performance.html")
print("✅ chart-price-vs-performance.html")

print("\nDone! 2 charts generated.")
