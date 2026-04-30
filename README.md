# 60632 Archer Heights — Industrial Corridor Intelligence

> **Hermes Agent Research Program** — A living, evolving intelligence repository for Chicago's 60632 industrial corridor (Archer Heights). Maintained by [Hermes Agent](https://hermes-agent.nousresearch.com), John Soprych's chief-of-staff.

## Mission

Become the definitive public intelligence resource on the 60632 / Archer Heights industrial corridor. This is not a one-off report — it's a **daily-updated research program** covering every business, property, development, rail connection, and economic driver in the area.

## Repository Structure

```
60632-archer-heights/
├── README.md              # This file — overview & mission
├── data/
│   ├── inventory.db        # SQLite database (837+ businesses)
│   └── exports/            # CSV/JSON exports of current data
├── research/
│   ├── companies/          # Deep dives on individual firms
│   ├── real-estate/        # Property listings, zoning, development
│   ├── rail/               # Rail infrastructure & intermodal
│   └── city-planning/      # Zoning, TIF, Moving Archer Forward
├── scripts/
│   ├── fetch-osm.py        # OSM data extraction
│   ├── enrich-db.py        # Research note insertion
│   └── report.py           # Report generation
├── reports/
│   ├── 2026-04-30-report.md  # Full initial report
│   └── daily/               # Daily status updates
├── sources/
│   ├── il-secstate.md      # IL Secretary of State business registry
│   ├── edgar.md            # SEC EDGAR filings (public companies)
│   └── cityofchicago.md    # Zoning, TIF, planning docs
└── AGENTS.md               # Hermes Agent instructions (auto-loaded)
```

## Current Coverage

| Category | Count | Status |
|----------|-------|--------|
| Total businesses catalogued (OSM) | 837 | ✅ Complete |
| Industrial/manufacturing | ~30+ | ✅ Identified |
| Deep-dive company profiles | ~15 | 🔄 In progress |
| Real estate listings | ~10 | ✅ Identified |
| Rail infrastructure | 3 major | ✅ Documented |
| Development pipeline | 4 projects | ✅ Documented |
| City planning context | Active | 🔄 In progress |

## Key Players

| Company | Revenue | Employees | Sector |
|---------|---------|-----------|--------|
| **Bagcraft Packaging (Novolex)** | $279M+ | ~1,200 | Foodservice packaging |
| **Chicago Metal Fabricators** | — | — | Metal fabrication (est. 1908) |
| **Chicago Metal Rolled Products** | — | — | Metal forming (est. 1908) |
| **Chicago American Manufacturing** | — | ~200 | Custom metal solutions (est. 1947) |
| **Vitner's (Utz Brands)** | $13.3M | 20-49 | Snack food distribution |
| **Lineage Cold Storage** | — | — | Cold-chain warehousing |

## Rail Infrastructure

- **BNSF Corwith Intermodal**: ~1 sq mi, 6 Class I railroads
- **Belt Railway of Chicago**: 28 mi mainline, 8,400 cars/day
- **Chicago Rail Link (OmniTRAX)**: 72 miles of switching track
- **7 intermodal yards** within 30 min of 4800 S Kilbourn

## Active Development Pipeline

- Sterling Bay: $25M, 147,500 SF spec industrial (4510 W Ann Lurie)
- "Moving Archer Forward": City of Chicago planning initiative
- Bridge Industrial: Ford City Mall → 913K SF warehouse redevelopment
- Greater Chicago Food Depository: Expansion underway

## How This Repo Works

This repo is maintained **programmatically by Hermes Agent**. Daily updates include:
1. New business discoveries from web research
2. Deep-dive company profiles
3. Real estate & development updates
4. City planning & zoning changes
5. Status reports emailed to stakeholder

The SQLite database at `data/inventory.db` is the canonical data store. All reports are generated from it.

---

*Maintained by Hermes Agent — elko.ai*
