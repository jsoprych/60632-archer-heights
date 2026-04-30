#!/usr/bin/env python3
"""
60632 Archer Heights — Enhanced Report Generator with ASCII Charts
Includes: biz type charts, property sizes, development pipeline, LLM price/performance
"""

import sqlite3
from datetime import datetime

db = sqlite3.connect("/opt/data/60632_business_inventory.db")
c = db.cursor()

c.execute("SELECT COUNT(*) FROM businesses")
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM research_notes")
notes_count = c.fetchone()[0]

c.execute("SELECT biz_type, COUNT(*) FROM businesses GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 12")
top_types = c.fetchall()

industrial_types = ('manufacturing','packaging_manufacturing','food_manufacturing',
                    'industrial','industrial_supply','industrial_property',
                    'cold_storage_warehouse','import_warehouse','warehouse',
                    'rail_intermodal','rail_switching','rail_services','recording_studio')
placeholders = ','.join('?' for _ in industrial_types)
c.execute(f"SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ({placeholders}) GROUP BY biz_type ORDER BY COUNT(*) DESC", industrial_types)
ind_data = c.fetchall()

c.execute(f"SELECT name, address, biz_type, description, website FROM businesses WHERE biz_type IN ({placeholders}) AND description != '' ORDER BY name", industrial_types)
detailed = c.fetchall()

c.execute("SELECT topic, note FROM research_notes")
notes = c.fetchall()
db.close()

def ascii_bar(labels, values, title="", width=30, sort=True):
    if not labels or not values:
        return ""
    data = list(zip(labels, values))
    if sort:
        data = sorted(data, key=lambda x: x[1], reverse=True)
    max_val = max(v for _, v in data)
    scale = width / max_val if max_val > 0 else 1
    lines = []
    if title:
        lines.append(f"  {title}")
        lines.append("  " + "-" * width)
    for label, val in data:
        bar_len = max(1, int(val * scale))
        bar = "█" * bar_len
        lines.append(f"  {label:<28} {bar} {val}")
    return "\n".join(lines)

def llm_section():
    """ASCII chart for LLM price/performance."""
    return """  ┌──────────────────────────────────────────────────────────────────────┐
  │  LLM PRICE / PERFORMANCE — US vs CHINESE PROVIDERS                 │
  │  (prices $/1M tokens, MMLU benchmark)                              │
  └──────────────────────────────────────────────────────────────────────┘

  BEST VALUE (under $1 in)
    Gemini 1.5 Flash ........ 0.08/0.30  MMLU 82.0  ████████████████░░
    Gemini 2.0 Flash ........ 0.10/0.40  MMLU 87.5  ████████████████████
    GPT-4o-mini ............. 0.15/0.60  MMLU 82.0  ████████████████░░
    DeepSeek-V3 🇨🇳 ......... 0.27/1.10  MMLU 88.5  ████████████████████½
    DeepSeek-R1 🇨🇳 ......... 0.55/2.19  MMLU 90.8  ████████████████████½

  MID-RANGE ($1-$5 in)
    Llama 3.1 70B .......... 0.59/0.79  MMLU 86.0  █████████████████░░
    Qwen2.5-72B 🇨🇳 ........ 0.90/0.90  MMLU 85.0  ████████████████░░░
    o3-mini ................ 1.10/4.40  MMLU 87.6  █████████████████░░
    Gemini 1.5 Pro ......... 1.25/5.00  MMLU 85.9  ████████████████░░░
    GPT-4o ................. 2.50/10.00 MMLU 88.7  ████████████████████
    Claude 3.5 Sonnet ...... 3.00/15.00 MMLU 88.7  ████████████████████

  PREMIUM ($5+ in)
    GPT-4 Turbo ............ 10.00/30.00  ——       █████████░░░░░░░░░░
    GPT-4.5 ................ 75.00/150.00 ——       ███░░░░░░░░░░░░░░░░

  ★ TOP PICK: DeepSeek-V3 — 88.5 MMLU @ $0.27/$1.10 = 9x cheaper than GPT-4o
  ★ TOP PICK: Gemini 2.0 Flash — 87.5 MMLU @ $0.10/$0.40 = 25x cheaper than GPT-4o
"""

# ── BUILD REPORT ──
print(f"""# 60632 Archer Heights — Daily Intelligence Report
**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Database:** {total} businesses | {notes_count} research notes

---
## 📊 AT A GLANCE

  Total businesses catalogued:  {total}
  Industrial/manufacturing:     {sum(v for _, v in ind_data)}
""")

print(ascii_bar([t for t,_ in top_types], [c_ for _,c_ in top_types], title=f"Business Types (n={total})", width=28))
print()
print(ascii_bar([t for t,_ in ind_data], [c_ for _,c_ in ind_data], title="Industrial & Manufacturing Breakdown", width=30))
print()

print("""
---
## 🏭 KEY INDUSTRIAL PLAYERS
""")
for name, addr, biz_type, desc, website in detailed:
    print(f"  **{name}**")
    if addr: print(f"  📍 {addr}")
    print(f"  🏷️  {biz_type.replace('_', ' ').title()}")
    if desc:
        short = desc if len(desc) < 130 else desc[:127] + "..."
        print(f"  ℹ️  {short}")
    if website: print(f"  🔗 {website}")
    print()

print("""
---
## 💼 CORPORATE OWNERSHIP HIGHLIGHTS

  **Bagcraft Packaging (Novolex)** — Apollo Global Management
  ● Revenue: ~$4.5B (pro-forma) | ~139 employees at 60632
  ● Pactiv Evergreen merger closed Apr 2025

  **Chicago Metal Fabricators** — $20.4M | Est. 1908 | ISO 9001
  **Chicago Metal Rolled Products** — $15.5M | Est. 1908
  **Chicago American Manufacturing** — $42.1M | GSA contract holder
""")

print("""
---
## 🏢 COMMERCIAL REAL ESTATE
""")
print(ascii_bar(
    ["4800 S Kilbourn Ave","Sterling Bay Warehouse","4500 S Tripp","4202 W 45th","4525 S Tripp","4601 S Tripp"],
    [237694,147500,92859,71004,17500,12983],
    title="Property Sizes (sq ft)", width=30
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
## 🤖 LLM PRICE / PERFORMANCE DASHBOARD
""")
print(llm_section())

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
""")
