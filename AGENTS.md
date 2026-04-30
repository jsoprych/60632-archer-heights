# Hermes Agent Instructions

This repo is maintained by **Hermes Agent** — John Soprych's autonomous chief-of-staff running on elko.ai's homelab infrastructure.

## What This Repo Is

A **living intelligence repository** for the 60632 / Archer Heights (Chicago) industrial corridor. Not a static report — a programmatically updated knowledge base that grows daily.

## Agent Protocol

### Daily Tasks
- [ ] Check for new business discoveries in 60632 (Brave search, news)
- [ ] Deep-dive one new company: revenue, employees, parent, website
- [ ] Monitor "Moving Archer Forward" city planning developments
- [ ] Check commercial real estate listings for 60632 industrial properties
- [ ] Run SQLite queries for status report

### Weekly
- [ ] Generate comprehensive weekly report
- [ ] Email status to johnsoprych@gmail.com
- [ ] Commit and push all changes to GitHub

### Database
- Primary store: `data/inventory.db` (SQLite)
- Schema: `businesses` table (name, address, lat, lon, biz_type, description, neighborhood, zip, source, website, phone, notes, created_at)
- Schema: `research_notes` table (topic, note, source_url, created_at)
- Always `INSERT OR IGNORE` by name+address to avoid duplicates

### Reporting
- Daily: short Telegram DM to John with key findings
- Full reports: emailed to johnsoprych@gmail.com, BCC to reid@elko.ai
- Reports include: count updates, new discoveries, notable properties

### Git Workflow
- Commit messages format: `[60632] Brief description — YYYY-MM-DD`
- Push after every meaningful update batch
- Never commit the raw OSM JSON (it's regenerable)

## Stakeholders

- **John Soprych** — CEO elko.ai, primary stakeholder
- **Patrick Gibbons** — family contact, receives reports
- **Diana Saldivar** — family contact, BCC on correspondence
