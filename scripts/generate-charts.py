#!/usr/bin/env python3
"""
Generate Concept-Diagrams style SVG charts for the 60632 report.
Produces standalone HTML files with auto dark/light mode.
"""

import sqlite3, os

DB = "/opt/data/60632_business_inventory.db"
OUT = "/opt/data/60632-archer-heights/reports/daily"
os.makedirs(OUT, exist_ok=True)

def q(sql):
    c = sqlite3.connect(DB).cursor()
    c.execute(sql)
    return c.fetchall()

def load_template():
    with open("/opt/data/60632-archer-heights/scripts/chart-template.html") as f:
        return f.read()

def save_html(title, subtitle, svg_content, filename):
    tpl = load_template()
    html = tpl.replace("<!-- DIAGRAM TITLE HERE -->", title)
    html = html.replace("<!-- OPTIONAL SUBTITLE HERE -->", subtitle)
    html = html.replace("<!-- PASTE SVG HERE -->", svg_content)
    path = os.path.join(OUT, filename)
    with open(path, "w") as f:
        f.write(html)
    return path

def bar_chart_svg(labels, values, colors, title="", height=200, bar_height=28, gap=8):
    """Generate a horizontal bar chart SVG using concept-diagrams design."""
    margin = {"t": 20, "r": 20, "b": 20, "l": 120}
    chart_w = 640 - margin["l"] - margin["r"]
    max_val = max(values)
    
    y = margin["t"]
    bars_svg = ""
    label_svg = ""
    val_svg = ""
    
    for label, val, color in zip(labels, values, colors):
        bar_w = int((val / max_val) * chart_w) if max_val > 0 else 0
        bar_w = max(bar_w, 4)  # minimum visible
        
        # Label on the left
        label_svg += f'  <text class="ts" x="{margin["l"] - 10}" y="{y + bar_height/2}" text-anchor="end" dominant-baseline="central">{label}</text>\n'
        # Bar
        bars_svg += f'  <rect x="{margin["l"]}" y="{y}" width="{bar_w}" height="{bar_height}" rx="4" class="{color}" stroke-width="0.5"/>\n'
        # Value on the right
        if val >= 1000:
            val_str = f"{val/1000:.0f}K"
        else:
            val_str = str(val)
        val_svg += f'  <text class="ts" x="{margin["l"] + bar_w + 8}" y="{y + bar_height/2}" dominant-baseline="central">{val_str}</text>\n'
        
        y += bar_height + gap
    
    total_h = y + margin["b"]
    
    return f'''<svg width="100%" viewBox="0 0 640 {total_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
            stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  {label_svg}
  {bars_svg}
  {val_svg}
</svg>'''

def revenue_chart_svg(data, height=180, bar_width=70, gap=30):
    """Vertical bar chart for revenue comparison."""
    margin = {"t": 30, "r": 20, "b": 50, "l": 50}
    chart_w = 640 - margin["l"] - margin["r"]
    max_val = max(v for _, v in data)
    
    bars = ""
    labels = ""
    vals = ""
    colors_cycle = ["c-purple", "c-teal", "c-coral", "c-pink", "c-blue", "c-green"]
    
    total_w = len(data) * bar_width + (len(data) - 1) * gap
    start_x = margin["l"] + (chart_w - total_w) // 2
    
    for i, (label, val) in enumerate(data):
        x = start_x + i * (bar_width + gap)
        bar_h = int((val / max_val) * (height - margin["t"] - margin["b"]))
        bar_h = max(bar_h, 6)
        y = margin["t"] + (height - margin["t"] - margin["b"]) - bar_h
        color = colors_cycle[i % len(colors_cycle)]
        
        bars += f'  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" rx="4" class="{color}" stroke-width="0.5"/>\n'
        # Short label
        short = label.replace("Chicago ", "").replace(" Manufacturing", " Mfg").replace("Ornamental ", "Orn. ")
        labels += f'  <text class="ts" x="{x + bar_width/2}" y="{height - margin["b"] + 16}" text-anchor="middle" dominant-baseline="central">{short}</text>\n'
        vals += f'  <text class="ts" x="{x + bar_width/2}" y="{y - 6}" text-anchor="middle" dominant-baseline="central">${val}M</text>\n'
    
    return f'''<svg width="100%" viewBox="0 0 640 {height}" xmlns="http://www.w3.org/2000/svg">
  {bars}
  {labels}
  {vals}
</svg>'''

def property_bar_svg(data, height=200):
    """Horizontal stacked bar for property sizes."""
    margin = {"t": 20, "r": 20, "b": 20, "l": 150}
    chart_w = 640 - margin["l"] - margin["r"]
    max_val = max(v for _, v in data)
    
    y = margin["t"]
    bar_height = 28
    gap = 8
    colors_cycle = ["c-teal", "c-purple", "c-coral", "c-pink", "c-blue", "c-amber"]
    
    svg = ""
    
    for i, (label, val) in enumerate(data):
        bar_w = int((val / max_val) * chart_w) if max_val > 0 else 0
        bar_w = max(bar_w, 4)
        color = colors_cycle[i % len(colors_cycle)]
        
        # Short labels
        short_label = label.replace("4800 S Kilbourn Ave", "4800 S Kilbourn").replace("Sterling Bay Warehouse", "Sterling Bay").replace("4500 S Tripp", "4500 S Tripp").replace("4202 W 45th", "4202 W 45th").replace("4525 S Tripp", "4525 S Tripp").replace("4601 S Tripp", "4601 S Tripp")
        
        svg += f'  <text class="ts" x="{margin["l"] - 10}" y="{y + bar_height/2}" text-anchor="end" dominant-baseline="central">{short_label}</text>\n'
        svg += f'  <rect x="{margin["l"]}" y="{y}" width="{bar_w}" height="{bar_height}" rx="4" class="{color}" stroke-width="0.5"/>\n'
        svg += f'  <text class="ts" x="{margin["l"] + bar_w + 8}" y="{y + bar_height/2}" dominant-baseline="central">{val:,} SF</text>\n'
        
        y += bar_height + gap
    
    total_h = y + margin["b"]
    return f'<svg width="100%" viewBox="0 0 640 {total_h}" xmlns="http://www.w3.org/2000/svg">\n{svg}\n</svg>'

# ════════════════════════════════════════
# GENERATE ALL CHARTS
# ════════════════════════════════════════

# 1. Business Types bar chart
types = q("SELECT biz_type, COUNT(*) FROM businesses GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 10")
labels = [t.replace("_", " ").title() for t, _ in types]
values = [v for _, v in types]
colors = ["c-purple", "c-teal", "c-coral", "c-pink", "c-blue", "c-green", "c-amber", "c-gray", "c-purple", "c-teal"]
svg1 = bar_chart_svg(labels, values, colors, title="Business Types")
save_html("Business Types — 60632 Archer Heights", f"{sum(values)} total businesses catalogued", svg1, "chart-business-types.html")
print(f"✅ chart-business-types.html — {len(types)} types")

# 2. Industrial breakdown
ind_types = ['manufacturing','packaging_manufacturing','food_manufacturing','industrial','industrial_supply','industrial_property','cold_storage_warehouse','import_warehouse','warehouse','recording_studio']
ind_data = q(f"SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ('" + "','".join(ind_types) + "') GROUP BY biz_type ORDER BY COUNT(*) DESC")
ind_labels = [t.replace("_", " ").title() for t, _ in ind_data]
ind_values = [v for _, v in ind_data]
ind_colors = ["c-coral", "c-purple", "c-teal", "c-pink", "c-blue", "c-amber", "c-green", "c-gray", "c-red", "c-coral"]
svg2 = bar_chart_svg(ind_labels, ind_values, ind_colors, title="Industrial & Manufacturing Breakdown")
save_html("Industrial & Manufacturing — 60632 Archer Heights", "Manufacturing intensity in the corridor", svg2, "chart-industrial.html")
print(f"✅ chart-industrial.html — {len(ind_data)} industrial types")

# 3. Revenue comparison
rev_data = [
    ("Chicago American Mfg", 42.1),
    ("Chicago Metal Fab", 20.4),
    ("CMRP", 15.5),
    ("Chicago Orn. Iron", 9.0),
    ("Archer Mfg", 3.1),
]
svg3 = revenue_chart_svg(rev_data)
save_html("Revenue Comparison — Metal Fabricators", "Estimated annual revenue ($M) from public sources", svg3, "chart-revenue.html")
print("✅ chart-revenue.html — 5 companies")

# 4. Property sizes
props = [
    ("4800 S Kilbourn Ave", 237694),
    ("Sterling Bay Warehouse", 147500),
    ("4500 S Tripp Ave", 92859),
    ("4202 W 45th St", 71004),
    ("4525 S Tripp Ave", 17500),
    ("4601 S Tripp Ave", 12983),
]
svg4 = property_bar_svg(props)
save_html("Industrial Property Sizes — 60632", "Largest available industrial properties in Archer Heights corridor", svg4, "chart-properties.html")
print("✅ chart-properties.html — 6 properties")

# 5. LLM Price/Performance chart
llm_labels = ["DeepSeek-V3 🇨🇳", "Gemini 2.0 Flash 🇺🇸", "DeepSeek-R1 🇨🇳", "Llama 3.1 70B 🇺🇸", "Qwen2.5-72B 🇨🇳", "GPT-4o-mini 🇺🇸", "GPT-4o 🇺🇸", "Claude 3.5 Sonnet 🇺🇸"]
llm_vals = [88.5, 87.5, 90.8, 86.0, 85.0, 82.0, 88.7, 88.7]
llm_prices = [0.27, 0.10, 0.55, 0.59, 0.90, 0.15, 2.50, 3.00]
llm_colors = ["c-coral", "c-blue", "c-red", "c-teal", "c-purple", "c-green", "c-amber", "c-pink"]

margin = {"t": 30, "r": 100, "b": 50, "l": 110}
chart_w = 640 - margin["l"] - margin["r"]
max_mmlu = max(llm_vals)
bar_h = 24
gap = 12

y = margin["t"]
svg5 = ""
for label, mmlu, price, color in zip(llm_labels, llm_vals, llm_prices, llm_colors):
    bar_w = int((mmlu / max_mmlu) * chart_w)
    svg5 += f'  <text class="ts" x="{margin["l"] - 10}" y="{y + bar_h/2}" text-anchor="end" dominant-baseline="central">{label}</text>\n'
    svg5 += f'  <rect x="{margin["l"]}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" class="{color}" stroke-width="0.5"/>\n'
    svg5 += f'  <text class="ts" x="{margin["l"] + chart_w + 8}" y="{y + bar_h/2}" dominant-baseline="central">MMLU {mmlu}  (${price}/M)</text>\n'
    y += bar_h + gap

total_h = y + margin["b"]
svg5_full = f'<svg width="100%" viewBox="0 0 640 {total_h}" xmlns="http://www.w3.org/2000/svg">\n{svg5}\n</svg>'
save_html("LLM Price/Performance — US vs Chinese Providers", "MMLU benchmark score vs input token price ($/1M tokens)", svg5_full, "chart-llm-price-performance.html")
print("✅ chart-llm-price-performance.html — 8 models")

print("\nDone! All charts generated.")
