# Quick Reference - HDB House Analyzer

## Your Simple Commands

### 🚀 Fastest Way (Auto-save JSON)
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token" --no-interactive
```
✅ Runs analysis  
✅ Auto-saves to: `house_analysis_1_3521_103_8198_TIMESTAMP.json`  
✅ No prompts  

---

### 📊 Save as CSV (for Excel)
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token" --format csv --no-interactive
```
✅ Saves CSV file  
✅ Open in Excel/Google Sheets  
✅ Sort by distance  

---

### 📝 Save as Markdown (for docs)
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token" --format markdown --no-interactive
```
✅ Formatted report  
✅ Nice tables  
✅ GitHub-ready  

---

### 💪 Save ALL Formats
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token" --format all --no-interactive
```
✅ Creates 3 files:  
- .json (for code)  
- .csv (for Excel)  
- .md (for docs)  

---

### 📁 Custom Filename
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token" --output my_report.json
```
✅ Saves to `my_report.json`  

---

## What Changed?

### Before:
```
❌ Had to answer prompts
❌ Only JSON format
❌ Manual filename
```

### Now:
```
✅ Use --no-interactive (no prompts!)
✅ Multiple formats (JSON/CSV/Markdown)
✅ Auto filenames with timestamp
✅ Perfect for automation
```

---

## Your Token

**Your access token:**
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ
```

**Expires:** Feb 13, 2026

---

## Examples

### Analyze Bishan HDB
```bash
python house_analyzer.py 1.3521 103.8198 \
  --token "eyJhbGc..." \
  --no-interactive
```

### Get CSV for Excel
```bash
python house_analyzer.py 1.3521 103.8198 \
  --token "eyJhbGc..." \
  --format csv \
  --output bishan_analysis.csv
```

### Full Analysis (all themes + all formats)
```bash
python house_analyzer.py 1.3521 103.8198 \
  --token "eyJhbGc..." \
  --all-themes \
  --format all \
  --no-interactive
```

---

## Flags Quick Reference

| Flag | What it does |
|------|--------------|
| `--token "xxx"` | Your access token (required) |
| `--no-interactive` | No prompts, auto-save |
| `--output file.json` | Save to specific file |
| `--format csv` | CSV format (or json, markdown, all) |
| `--all-themes` | Use all 100+ themes (more data) |
| `--radius 10` | Search radius in km |

---

## Files You'll Get

### Auto-generated filename:
```
house_analysis_1_3521_103_8198_20260211_092000.json
                ↑       ↑        ↑
              latitude longitude timestamp
```

### With custom name:
```bash
--output my_report.json    # Creates: my_report.json
--output data/analysis     # Creates: data/analysis.json (adds .json)
```

### With --format all:
```bash
--output report --format all
# Creates:
#   report.json
#   report.csv
#   report.md
```

---

## Need Help?

**See full guide:** OUTPUT_FORMATS_GUIDE.md

**Quick token guide:** HOW_TO_USE_YOUR_TOKEN.md

**Troubleshooting:** TROUBLESHOOTING.md

---

## Most Common Command (Copy This!)

```bash
python house_analyzer.py 1.3521 103.8198 \
  --token "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ" \
  --no-interactive
```

**Done!** Analysis runs and saves automatically! ✅

---

*Replace coordinates `1.3521 103.8198` with your location*
