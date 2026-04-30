#!/usr/bin/env python3
"""
Proper SVG chart generator using concept-diagrams design system.
Produces standalone HTML files with real axis math, proper CSS, auto dark/light mode.
"""

import sqlite3, os

DB = "/opt/data/60632_business_inventory.db"
OUT = "/opt/data/60632-archer-heights/reports/daily"
TPL = "/opt/data/60632-archer-heights/scripts/concept-template.html"
os.makedirs(OUT, exist_ok=True)

def q(sql, params=None):
    c = sqlite3.connect(DB).cursor()
    if params:
        c.execute(sql, params)
    else:
        c.execute(sql)
    return c.fetchall()

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
# CHART 1: Business Types — Horizontal Bar Chart
# ═══════════════════════════════════════════════════════════════

types = q("SELECT biz_type, COUNT(*) FROM businesses GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 10")
max_val = max(v for _, v in types)
n = len(types)

# Layout: 680x(60 + n*40 + 40)
CHART_L = 120   # left margin for labels
CHART_R = 60    # right margin for values
CHART_W = 680 - CHART_L - CHART_R  # 500
CHART_T = 40
BAR_H = 24
GAP = 14
H = CHART_T + n * (BAR_H + GAP) + 30

colors = ["c-purple", "c-teal", "c-coral", "c-pink", "c-blue", "c-green", "c-amber", "c-gray", "c-purple", "c-teal"]

bars = ""
for i, (label, val) in enumerate(types):
    y = CHART_T + i * (BAR_H + GAP)
    w = int((val / max_val) * CHART_W) if max_val else 0
    w = max(w, 6)
    c = colors[i % len(colors)]
    display = label.replace("_", " ").title()
    bars += f'  <text class="ts" x="{CHART_L - 12}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{display}</text>\n'
    bars += f'  <rect class="{c}" x="{CHART_L}" y="{y}" width="{w}" height="{BAR_H}" rx="4" stroke-width="0.75"/>\n'
    bars += f'  <text class="t" x="{CHART_L + w + 8}" y="{y + BAR_H/2}" dominant-baseline="central">{val}</text>\n'

svg1 = f'''<svg width="100%" viewBox="0 0 680 {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
{bars}
</svg>'''

save_html("Business Types — 60632 Archer Heights", f"{sum(v for _, v in types)} total businesses", svg1, "chart-biz-types.html")
print("✅ chart-biz-types.html")

# ═══════════════════════════════════════════════════════════════
# CHART 2: Industrial Breakdown — Horizontal Bars
# ═══════════════════════════════════════════════════════════════

ind_types = ['manufacturing','packaging_manufacturing','food_manufacturing','industrial',
             'industrial_supply','industrial_property','cold_storage_warehouse',
             'import_warehouse','warehouse','recording_studio']
placeholders = ','.join('?' for _ in ind_types)
ind_data = q(f"SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ({placeholders}) GROUP BY biz_type ORDER BY COUNT(*) DESC", ind_types)
ind_total = sum(v for _, v in ind_data)
ind_max = max(v for _, v in ind_data)

ind_colors = ["c-coral", "c-purple", "c-teal", "c-pink", "c-blue", "c-amber", "c-green", "c-gray", "c-red", "c-coral"]
n2 = len(ind_data)
H2 = CHART_T + n2 * (BAR_H + GAP) + 30

bars2 = ""
for i, (label, val) in enumerate(ind_data):
    y = CHART_T + i * (BAR_H + GAP)
    w = int((val / ind_max) * CHART_W) if ind_max else 0
    w = max(w, 6)
    c = ind_colors[i % len(ind_colors)]
    display = label.replace("_", " ").title()
    bars2 += f'  <text class="ts" x="{CHART_L - 12}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{display}</text>\n'
    bars2 += f'  <rect class="{c}" x="{CHART_L}" y="{y}" width="{w}" height="{BAR_H}" rx="4" stroke-width="0.75"/>\n'
    bars2 += f'  <text class="t" x="{CHART_L + w + 8}" y="{y + BAR_H/2}" dominant-baseline="central">{val}</text>\n'

svg2 = f'''<svg width="100%" viewBox="0 0 680 {H2}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
{bars2}
</svg>'''

save_html("Industrial & Manufacturing — 60632 Archer Heights", f"{ind_total} industrial-classified businesses", svg2, "chart-industrial.html")
print("✅ chart-industrial.html")

# ═══════════════════════════════════════════════════════════════
# CHART 3: Revenue Comparison — Vertical Bars
# ═══════════════════════════════════════════════════════════════

rev_data = [
    ("Chicago American\nManufacturing", 42.1),
    ("Chicago Metal\nFabricators", 20.4),
    ("CMRP", 15.5),
    ("Chicago Orn.\nIron / COI", 9.0),
    ("Archer\nManufacturing", 3.1),
]
rev_max = max(v for _, v in rev_data)
n3 = len(rev_data)
BAR_W = 64
GAP3 = 32
total_w = n3 * BAR_W + (n3 - 1) * GAP3
start_x = (680 - total_w) // 2
CHART_B3 = 60
CHART_H3 = 300  # available height from top
H3 = CHART_H3 + 100

bars3 = ""
y_axis_vals = ""
for i, (label, val) in enumerate(rev_data):
    x = start_x + i * (BAR_W + GAP3)
    bh = int((val / rev_max) * (CHART_H3 - 30))
    bh = max(bh, 6)
    y = (CHART_H3 - 30) - bh + 30
    c = ["c-coral", "c-blue", "c-teal", "c-purple", "c-pink"][i]
    bars3 += f'  <rect class="{c}" x="{x}" y="{y}" width="{BAR_W}" height="{bh}" rx="4" stroke-width="0.75"/>\n'
    # Value above bar
    bars3 += f'  <text class="ts" x="{x + BAR_W/2}" y="{y - 6}" text-anchor="middle" dominant-baseline="central">${val}M</text>\n'
    # Label below
    lines = label.split("\n")
    for li, line in enumerate(lines):
        bars3 += f'  <text class="ts" x="{x + BAR_W/2}" y="{CHART_H3 - 30 + 45 + li*16}" text-anchor="middle" dominant-baseline="central">{line}</text>\n'

# Y axis labels
for v in [0, 10, 20, 30, 40]:
    y = (CHART_H3 - 30) - int((v / rev_max) * (CHART_H3 - 30)) + 30
    bars3 += f'  <text class="ts" x="55" y="{y}" text-anchor="end" dominant-baseline="central">${v}M</text>\n'
    bars3 += f'  <line x1="65" y1="{y}" x2="72" y2="{y}" class="leader" stroke-width="0.5"/>\n'

svg3 = f'''<svg width="100%" viewBox="0 0 680 {H3}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <text class="ts" x="55" y="16" text-anchor="end" dominant-baseline="central">Revenue</text>
{bars3}
</svg>'''

save_html("Revenue Comparison — Metal Fabricators in 60632", "Estimated annual revenue ($M) from public sources", svg3, "chart-revenue.html")
print("✅ chart-revenue.html")

# ═══════════════════════════════════════════════════════════════
# CHART 4: Property Sizes — Horizontal Bars
# ═══════════════════════════════════════════════════════════════

props = [
    ("4800 S Kilbourn Ave", 237694),
    ("Sterling Bay (4510 W Ann Lurie)", 147500),
    ("4500 S Tripp Ave", 92859),
    ("4202 W 45th St", 71004),
    ("4525 S Tripp Ave", 17500),
    ("4601 S Tripp Ave", 12983),
]
prop_max = max(v for _, v in props)
n4 = len(props)
CHART_L4 = 160
CHART_W4 = 680 - CHART_L4 - CHART_R
H4 = CHART_T + n4 * (BAR_H + GAP) + 30
prop_colors = ["c-teal", "c-purple", "c-coral", "c-pink", "c-blue", "c-amber"]

bars4 = ""
for i, (label, val) in enumerate(props):
    y = CHART_T + i * (BAR_H + GAP)
    w = int((val / prop_max) * CHART_W4)
    w = max(w, 6)
    c = prop_colors[i]
    sf = f"{val:,}"
    bars4 += f'  <text class="ts" x="{CHART_L4 - 12}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{label}</text>\n'
    bars4 += f'  <rect class="{c}" x="{CHART_L4}" y="{y}" width="{w}" height="{BAR_H}" rx="4" stroke-width="0.75"/>\n'
    bars4 += f'  <text class="t" x="{CHART_L4 + w + 8}" y="{y + BAR_H/2}" dominant-baseline="central">{sf} SF</text>\n'

# Legend
legend_y = H4 - 10
bars4 += f'  <text class="ts" x="60" y="{legend_y}" dominant-baseline="central">● Largest listing: 4800 S Kilbourn — 237,694 SF with 15-ton cranes</text>\n'
bars4 += f'  <text class="ts" x="60" y="{legend_y + 18}" dominant-baseline="central">● Sterling Bay: $25M spec industrial, Class 6b tax incentive approved</text>\n'
H4 += 56

svg4 = f'''<svg width="100%" viewBox="0 0 680 {H4}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
{bars4}
</svg>'''

save_html("Industrial Property Sizes — 60632", "Largest available industrial properties in Archer Heights corridor", svg4, "chart-properties.html")
print("✅ chart-properties.html")

# ═══════════════════════════════════════════════════════════════
# CHART 5: LLM Price/Performance — Horizontal Bars with dual info
# ═══════════════════════════════════════════════════════════════

llm_data = [
    ("DeepSeek-V3 🇨🇳", 88.5, 0.27, "c-coral"),
    ("DeepSeek-R1 🇨🇳", 90.8, 0.55, "c-red"),
    ("Gemini 2.0 Flash 🇺🇸", 87.5, 0.10, "c-blue"),
    ("GPT-4o-mini 🇺🇸", 82.0, 0.15, "c-green"),
    ("Llama 3.1 70B 🇺🇸", 86.0, 0.59, "c-teal"),
    ("Qwen2.5-72B 🇨🇳", 85.0, 0.90, "c-purple"),
    ("GPT-4o 🇺🇸", 88.7, 2.50, "c-amber"),
    ("Claude 3.5 Sonnet 🇺🇸", 88.7, 3.00, "c-pink"),
]
llm_max = max(v for _, v, _, _ in llm_data)
n5 = len(llm_data)
CHART_L5 = 140
CHART_W5 = 680 - CHART_L5 - 180  # 360 for bars, rest for labels
H5 = CHART_T + n5 * (BAR_H + GAP) + 40

bars5 = ""
for i, (name, mmlu, price, c) in enumerate(llm_data):
    y = CHART_T + i * (BAR_H + GAP)
    w = int((mmlu / llm_max) * CHART_W5)
    w = max(w, 6)
    bars5 += f'  <text class="ts" x="{CHART_L5 - 12}" y="{y + BAR_H/2}" text-anchor="end" dominant-baseline="central">{name}</text>\n'
    bars5 += f'  <rect class="{c}" x="{CHART_L5}" y="{y}" width="{w}" height="{BAR_H}" rx="4" stroke-width="0.75"/>\n'
    bars5 += f'  <text class="ts" x="{CHART_L5 + CHART_W5 + 12}" y="{y + BAR_H/2}" dominant-baseline="central">MMLU {mmlu}  ${price:.2f}/M in</text>\n'

# Bottombar: value picks
H5 += 50
bars5 += f'  <text class="th" x="60" y="{H5 - 30}" dominant-baseline="central">★ Best Value: DeepSeek-V3 — 88.5 MMLU @ $0.27/M (9x cheaper than GPT-4o)</text>\n'
bars5 += f'  <text class="th" x="60" y="{H5 - 12}" dominant-baseline="central">★ Best US Value: Gemini 2.0 Flash — 87.5 MMLU @ $0.10/M (25x cheaper than GPT-4o)</text>\n'

svg5 = f'''<svg width="100%" viewBox="0 0 680 {H5}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <text class="ts" x="{CHART_L5 + CHART_W5 + 12}" y="20" dominant-baseline="central">MMLU Score → | Price per 1M tokens</text>
{bars5}
</svg>'''

save_html("LLM Price/Performance — US vs Chinese Providers", "MMLU benchmark score vs input token price ($/1M tokens)", svg5, "chart-llm-price-performance.html")
print("✅ chart-llm-price-performance.html")

print("\nAll charts regenerated with proper SVG layout math.")
