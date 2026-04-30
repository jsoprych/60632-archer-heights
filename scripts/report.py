#!/usr/bin/env python3
"""
60632 Archer Heights — Enhanced Report Generator with ASCII Charts
Run by Hermes Agent. Generates markdown report from SQLite database.
"""

import sqlite3
from datetime import datetime
from collections import Counter

db = sqlite3.connect("/opt/data/60632_business_inventory.db")
c = db.cursor()

c.execute("SELECT COUNT(*) FROM businesses")
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM research_notes")
notes_count = c.fetchone()[0]

c.execute("SELECT topic, note FROM research_notes")
notes = c.fetchall()

# --- ASCII Bar Chart Helper ---
def ascii_bar(labels, values, title="", width=30, sort=True):
    """Generate an ASCII bar chart for plain-text reports."""
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
        label_clean = label.replace("_", " ").title()
        lines.append(f"  {label_clean:<25} {bar} {val}")
    
    return "\n".join(lines)

# --- Business Type Breakdown ---
c.execute("""
    SELECT biz_type, COUNT(*) FROM businesses 
    GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 15
""")
type_data = c.fetchall()

# --- Industrial / Manufacturing ---
industrial_types = ('manufacturing','packaging_manufacturing','food_manufacturing',
                    'industrial','industrial_supply','industrial_property',
                    'cold_storage_warehouse','import_warehouse','warehouse',
                    'rail_intermodal','rail_switching','rail_services','recording_studio')

placeholders = ','.join('?' for _ in industrial_types)
c.execute(f"SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ({placeholders}) GROUP BY biz_type ORDER BY COUNT(*) DESC", industrial_types)
ind_data = c.fetchall()

# --- Top 10 Industries by type counts ---
c.execute("SELECT biz_type, COUNT(*) FROM businesses GROUP BY biz_type ORDER BY COUNT(*) DESC LIMIT 10")
top10 = c.fetchall()

# --- New businesses in last 7 days ---
c.execute("SELECT COUNT(*) FROM businesses WHERE created_at >= datetime('now', '-7 days')")
new_7 = c.fetchone()[0]

c.execute("SELECT name, address, biz_type, description, website FROM businesses WHERE biz_type IN ({p}) AND description != '' ORDER BY name".format(p=placeholders), industrial_types)
detailed = c.fetchall()

db.close()

# --- BUILD REPORT ---

print(f"""# 60632 Archer Heights — Daily Intelligence Report
**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Database:** {total} businesses | {notes_count} research notes

---
## 📊 AT A GLANCE
""")

print(f"  Total businesses catalogued:  {total}")
print(f"  New in last 7 days:          {new_7}")
print(f"  Industrial/manufacturing:     {sum(v for _, v in ind_data)}")
print()

# Business type breakdown chart
print(ascii_bar(
    [t for t, _ in top10],
    [c_ for _, c_ in top10],
    title=f"Top Business Types (n={total})",
    width=25
))
print()

# Industrial breakdown chart
print(ascii_bar(
    [t for t, _ in ind_data],
    [c_ for _, c_ in ind_data],
    title=f"Industrial & Manufacturing Breakdown",
    width=30
))
print()

# --- KEY INDUSTRIAL PLAYERS ---
print("""
---
## 🏭 KEY INDUSTRIAL PLAYERS
""")

for name, addr, biz_type, desc, website in detailed:
    print(f"  **{name}**")
    if addr:
        print(f"  📍 {addr}")
    print(f"  🏷️  {biz_type.replace('_', ' ').title()}")
    if desc:
        # Truncate long descriptions for brevity
        short = desc if len(desc) < 120 else desc[:117] + "..."
        print(f"  ℹ️  {short}")
    if website:
        print(f"  🔗 {website}")
    print()

# --- CORPORATE OWNERSHIP ---
print("""
---
## 💼 CORPORATE OWNERSHIP HIGHLIGHTS
""")
print("""  **Bagcraft Packaging (Novolex)**
  ● Parent: Apollo Global Management (~$6B buyout, 2022)
  ● Novolex revenue: ~$4.5B (pro-forma post-Pactiv)
  ● Bagcraft revenue: ~$279M | ~139 employees at 3900 W 43rd
  ● Pactiv Evergreen merger closed Apr 2025

  **Chicago Metal Fabricators** — Founded 1908 | $20.4M | IS0 9001:2015
  **Chicago Metal Rolled Products** — Founded 1908 | $15.5M | World's largest beam bender
  **Chicago American Manufacturing** — $42.1M | GSA contract holder
""")

# --- REAL ESTATE ---
print("""
---
## 🏢 COMMERCIAL REAL ESTATE
""")
print(ascii_bar(
    ["4800 S Kilbourn Ave", "Sterling Bay Warehouse", "4500 S Tripp", "4202 W 45th", "4525 S Tripp", "4601 S Tripp"],
    [237694, 147500, 92859, 71004, 17500, 12983],
    title="Property Sizes (sq ft)",
    width=30
))
print()

# --- DEVELOPMENT TIMELINE ---
print("""
---
## 🏗️ DEVELOPMENT PIPELINE
""")
print("""  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
  Sterling Bay Warehouse ........... 147,500 SF  ████████████████ UNDERWAY
  Greater Chicago Food Depository .. Expansion   ████████████████ UNDERWAY
  Moving Archer Forward ........... Corridor     ████████████░░░ ACTIVE
  Bridge Ind / Ford City Mall ..... 913,000 SF   ████░░░░░░░░░░░ PROPOSED
  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
""")

# --- RESEARCH NOTES ---
print("""
---
## 📓 RESEARCH NOTES
""")

for topic, note in notes:
    short = note if len(note) < 200 else note[:197] + "..."
    print(f"  **{topic.replace('_', ' ').title()}**")
    print(f"  {short}")
    print()

# --- NEXT ACTIONS ---
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
