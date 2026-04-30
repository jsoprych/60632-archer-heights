#!/usr/bin/env python3
"""
60632 Archer Heights — Daily Status Generator
Run by Hermes Agent. Generates markdown report from SQLite database.
"""

import sqlite3, json
from datetime import datetime

db = sqlite3.connect("/opt/data/60632_business_inventory.db")
c = db.cursor()

c.execute("SELECT COUNT(*) FROM businesses")
total = c.fetchone()[0]

c.execute("SELECT biz_type, COUNT(*) FROM businesses WHERE biz_type IN ('manufacturing','packaging_manufacturing','food_manufacturing','industrial','industrial_supply','industrial_property','cold_storage_warehouse','import_warehouse') GROUP BY biz_type ORDER BY COUNT(*) DESC")
industrial = c.fetchall()

c.execute("SELECT COUNT(*) FROM research_notes")
notes_count = c.fetchone()[0]

c.execute("SELECT topic, note FROM research_notes")
notes = c.fetchall()

c.execute("SELECT name, address, biz_type, description FROM businesses WHERE biz_type IN ('manufacturing','packaging_manufacturing','food_manufacturing','industrial_property','cold_storage_warehouse') AND description != '' ORDER BY name")
detailed = c.fetchall()

db.close()

print(f"""# 60632 Archer Heights — Status Report
**Date:** {datetime.now().strftime('%B %d, %Y')}

## Database Snapshot
- **Total businesses:** {total}
- **Research notes:** {notes_count}
- **Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

## Industrial & Manufacturing Breakdown
""")

for t, c_ in industrial:
    print(f"- **{t}:** {c_}")

print(f"""
## Key Industrial Players
""")

for name, addr, biz_type, desc in detailed:
    print(f"### {name}")
    print(f"- **Address:** {addr}")
    print(f"- **Type:** {biz_type}")
    print(f"- **Description:** {desc}")
    print()

print("""## Research Topics
""")

for topic, note in notes:
    print(f"### {topic}")
    print(f"{note}")
    print()

print("""## Next Actions
- [ ] Deep-dive: Novolex/Bagcraft parent financials via EDGAR
- [ ] Search IL Secretary of State business registry for 60632
- [ ] Check "Moving Archer Forward" public meeting schedule
- [ ] Cross-reference OSM data with Google Maps for completeness
- [ ] Pull individual company websites and contact info""")
