#!/usr/bin/env python3
"""
60632 Archer Heights — Daily Report Generator
Generates: chart HTMLs (concept-diagrams SVGs) + markdown report + inlines ASCII fallback
"""

import sqlite3, os, subprocess
from datetime import datetime

DB = "/opt/data/60632_business_inventory.db"
REPO = "/opt/data/60632-archer-heights"

db = sqlite3.connect(DB)
c = db.cursor()

c.execute("SELECT COUNT(*) FROM businesses")
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM research_notes")
notes_count = c.fetchone()[0]

c.execute("SELECT biz_type, COUNT(*) FROM businesses GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 12")
top_types = c.fetchall()

ind_types = ('manufacturing','packaging_manufacturing','food_manufacturing',
             'industrial','industrial_supply','industrial_property',
             'cold_storage_warehouse','import_warehouse','warehouse',
             'rail_intermodal','rail_switching','rail_services','recording_studio')
placeholders = ','.join('?' for _ in ind_types)
c.execute(f"SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ({placeholders}) GROUP BY biz_type ORDER BY COUNT(*) DESC", ind_types)
ind_data = c.fetchall()

c.execute(f"SELECT name, address, biz_type, description, website FROM businesses WHERE biz_type IN ({placeholders}) AND description != '' ORDER BY name", ind_types)
detailed = c.fetchall()

c.execute("SELECT topic, note FROM research_notes")
notes = c.fetchall()
db.close()

# Generate charts
print("Generating SVG charts...")
subprocess.run(["python3", os.path.join(REPO, "scripts", "generate-charts.py")], cwd=REPO)

def ascii_bar(labels, values, title="", width=28, sort=True):
    if not labels or not values: return ""
    data = sorted(zip(labels, values), key=lambda x: x[1], reverse=True) if sort else list(zip(labels, values))
    max_val = max(v for _, v in data)
    scale = width / max_val if max_val > 0 else 1
    lines = []
    if title: lines.append(f"  {title}"); lines.append("  " + "-" * width)
    for label, val in data:
        bar_len = max(1, int(val * scale))
        lines.append(f"  {label:<28} {'█' * bar_len} {val}")
    return "\n".join(lines)

# ── BUILD REPORT ──
print(f"""
# 60632 Archer Heights — Daily Intelligence Report
**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Database:** {total} businesses | {notes_count} research notes
**Charts:** View in browser (drag HTML files into any browser)

---
## 📊 AT A GLANCE

  Total businesses catalogued:  {total}
  Industrial/manufacturing:     {sum(v for _, v in ind_data)}

[📈 Business Types Chart](reports/daily/chart-business-types.html)
[🏭 Industrial Breakdown Chart](reports/daily/chart-industrial.html)
[💰 Revenue Comparison](reports/daily/chart-revenue.html)
[🏢 Property Sizes](reports/daily/chart-properties.html)
[🤖 LLM Price/Performance](reports/daily/chart-llm-price-performance.html)
""")

print(ascii_bar([t for t,_ in top_types], [c_ for _,c_ in top_types], title=f"Business Types (n={total})"))
print()
print(ascii_bar([t for t,_ in ind_data], [c_ for _,c_ in ind_data], title="Industrial & Manufacturing Breakdown"))
print()

print("""
---
## 🏭 KEY INDUSTRIAL PLAYERS
""")
for name, addr, biz_type, desc, website in detailed:
    print(f"  **{name}**")
    if addr: print(f"  📍 {addr}")
    print(f"  🏷️  {biz_type.replace('_', ' ').title()}")
    if desc: print(f"  ℹ️  {desc[:130]}")
    if website: print(f"  🔗 {website}")
    print()

print("""
---
## 💼 CORPORATE OWNERSHIP HIGHLIGHTS

  **Bagcraft Packaging (Novolex)** — Apollo Global Management
  ● Revenue: ~$4.5B (pro-forma) | ~139 employees at 60632
  ● Pactiv Evergreen merger closed Apr 2025

  **Chicago Metal Fabricators** — $20.4M | Est. 1908 | ISO 9001
  **Chicago Metal Rolled Products** — $15.5M | Est. 1908 | World's largest beam bender
  **Chicago American Manufacturing** — $42.1M | GSA contract holder
""")

print("""
---
## 🏢 COMMERCIAL REAL ESTATE
""")
print(ascii_bar(
    ["4800 S Kilbourn Ave","Sterling Bay","4500 S Tripp","4202 W 45th","4525 S Tripp","4601 S Tripp"],
    [237694,147500,92859,71004,17500,12983],
    title="Property Sizes (sq ft)"
))
print("""
  ● 4800 S Kilbourn: 237,694 SF | 15-ton cranes | 7 intermodal yards
  ● Sterling Bay: 147,500 SF | $25M | Class 6b approved
  ● Tripp Corridor: multiple flex spaces $8.95-$9.50/SF/YR
""")

print("""
---
## 🏗️ DEVELOPMENT PIPELINE
  Sterling Bay Warehouse ........... 147,500 SF  ████████████████ UNDERWAY
  Greater Chicago Food Depository .. Expansion   ████████████████ UNDERWAY
  Moving Archer Forward ........... Corridor     ████████████░░░ ACTIVE
  Bridge Ind / Ford City Mall ..... 913,000 SF   ████░░░░░░░░░░░ PROPOSED
""")

print("""
---
## 🤖 LLM PRICE / PERFORMANCE
""")
print("""  ★ TOP PICK: DeepSeek-V3 — 88.5 MMLU @ $0.27/M — 9x cheaper than GPT-4o
  ★ TOP PICK: Gemini 2.0 Flash — 87.5 MMLU @ $0.10/M — 25x cheaper than GPT-4o

  Model                Input$  Output$  MMLU   Value
  DeepSeek-V3 🇨🇳       0.27    1.10    88.5   ████████████████████
  DeepSeek-R1 🇨🇳       0.55    2.19    90.8   ████████████████░░
  Gemini 2.0 Flash 🇺🇸  0.10    0.40    87.5   ██████████████████░
  GPT-4o-mini 🇺🇸       0.15    0.60    82.0   █████████████░░░░░
  Llama 3.1 70B 🇺🇸     0.59    0.79    86.0   ██████████████░░░░
  Qwen2.5-72B 🇨🇳       0.90    0.90    85.0   █████████████░░░░░
  GPT-4o 🇺🇸            2.50   10.00    88.7   ██████████████████░
  Claude 3.5 Sonnet 🇺🇸 3.00   15.00    88.7   ██████████████████░

  [📈 Full LLM Chart](reports/daily/chart-llm-price-performance.html)
""")

print("""
---
## 📓 RESEARCH NOTES
""")
for topic, note in notes:
    short = note if len(note) < 200 else note[:197] + "..."
    print(f"  **{topic.replace('_',' ').title()}**")
    print(f"  {short}")
    print()

print("""
---
## 📋 NEXT ACTIONS
  [ ] IL Secretary of State business registry cross-reference
  [ ] Vitner's/Utz Brands financials
  [ ] Phone numbers for every industrial business
  [ ] WARN notice monitoring for 60632
  [ ] Moving Archer Forward meeting calendar
  [ ] Cook County property tax records
  [ ] Federal contracts database (SAM.gov)

---
*Generated by Hermes Agent — github.com/jsoprych/60632-archer-heights*
  *Charts: concept-diagrams SVG — open *.html files in any browser*
""")
