# Output Formats Guide

## Overview

The HDB House Analyzer now supports multiple output formats for saving analysis results:
- **JSON** - Complete data structure (programmatic use)
- **CSV** - Tabular format (spreadsheets)
- **Markdown** - Formatted report (documentation)

## Quick Start

### Automatic Output (No Prompts)

```bash
# Auto-save as JSON with timestamp filename
python house_analyzer.py 1.3521 103.8198 --token "your_token" --no-interactive

# Creates: house_analysis_1_3521_103_8198_20260211_092000.json
```

### Save to Specific File

```bash
# Save as JSON
python house_analyzer.py 1.3521 103.8198 --token "xxx" --output my_report.json

# Save as CSV
python house_analyzer.py 1.3521 103.8198 --token "xxx" --output my_report.csv --format csv

# Save as Markdown
python house_analyzer.py 1.3521 103.8198 --token "xxx" --output my_report.md --format markdown

# Save in ALL formats at once
python house_analyzer.py 1.3521 103.8198 --token "xxx" --output my_report --format all
# Creates: my_report.json, my_report.csv, my_report.md
```

## Command-Line Flags

### `--output, -o <filename>`
Specify output file path.
- If not specified with `--no-interactive`, auto-generates timestamp-based filename
- Extension is auto-added based on format if missing

**Examples:**
```bash
--output report.json          # Saves to report.json
--output data/report          # Auto-adds extension based on format
-o analysis                   # Short form
```

### `--format, -f <format>`
Choose output format(s).

**Options:**
- `json` - JSON format (default)
- `csv` - CSV/spreadsheet format
- `markdown` or `md` - Markdown report
- `all` - Save in all formats

**Examples:**
```bash
--format json                 # JSON format
--format csv                  # CSV format
--format markdown             # Markdown format
--format all                  # All three formats
-f csv                        # Short form
```

### `--no-interactive`
Disable interactive prompts, automatically save output.
- Auto-generates filename with timestamp if `--output` not specified
- Uses `--format` choice (defaults to JSON)
- Perfect for batch processing and automation

**Example:**
```bash
python house_analyzer.py 1.3521 103.8198 --token "xxx" --no-interactive --format csv
# Runs analysis and saves CSV without any prompts
```

## Output Formats Explained

### 1. JSON Format

**Best for:**
- Programmatic access
- APIs and web services
- Data processing scripts
- Preserving complete data structure

**Features:**
- Complete nested data structure
- All fields preserved
- Easy to parse programmatically
- Machine-readable

**Sample Output:**
```json
{
  "latitude": 1.3521,
  "longitude": 103.8198,
  "address": "123 Bishan Street",
  "public_transport": {
    "mrt_stations": [
      {
        "name": "BISHAN MRT STATION",
        "id": "CC15",
        "distance_km": 0.456,
        "distance_m": 456,
        "latitude": 1.3506,
        "longitude": 103.8499
      }
    ]
  },
  "amenities": {
    "kindergartens": [...],
    "parks": [...]
  }
}
```

### 2. CSV Format

**Best for:**
- Excel/Google Sheets
- Data analysis
- Sorting and filtering
- Quick review

**Features:**
- Tabular format
- Easy to sort by distance
- Import into spreadsheets
- Simple structure

**Sample Output:**
```csv
Category,Name,Distance (km),Distance (m),Details
Location,123 Bishan Street,,,Lat: 1.3521, Lon: 103.8198

PUBLIC TRANSPORT - MRT STATIONS
MRT,BISHAN MRT STATION,0.456,456,CC15
MRT,ANG MO KIO MRT STATION,1.234,1234,NS16

PUBLIC TRANSPORT - BUS STOPS
Bus Stop,Opp Blk 283,0.123,123,54321
Bus Stop,Blk 284,0.156,156,54322

AMENITY - KINDERGARTENS
kindergartens,Little Skool-House,0.345,345,123 Street
```

**Usage in Excel:**
1. Open Excel
2. File → Open → Select CSV file
3. Data will be formatted in columns
4. Can sort by "Distance (km)" column

### 3. Markdown Format

**Best for:**
- Documentation
- Reports
- Sharing on GitHub/GitLab
- Human-readable formatted text

**Features:**
- Formatted tables
- Headers and sections
- GitHub-compatible
- Easy to read

**Sample Output:**
```markdown
# 🏠 HDB House Analysis Report

**Generated:** 2026-02-11 09:20:00

## 📍 Location Information

**Address:** 123 Bishan Street

**Coordinates:** 1.3521, 103.8198

**Planning Area:** BISHAN

## 📊 Summary

- **Total Amenities Found:** 45
- **Nearest MRT:** BISHAN MRT STATION (0.46 km)
- **Nearest Bus Stop:** Opp Blk 283 (0.12 km)

## 🚇🚌 Public Transport

### MRT Stations

| Name | Distance | ID |
|------|----------|-----|
| BISHAN MRT STATION | 0.46 km | CC15 |
| ANG MO KIO MRT STATION | 1.23 km | NS16 |

### Bus Stops

| Name | Distance | ID |
|------|----------|-----|
| Opp Blk 283 | 0.12 km | 54321 |
| Blk 284 | 0.16 km | 54322 |
```

## Batch Processing Examples

### Process Multiple Locations

```bash
#!/bin/bash
# analyze_multiple.sh

LOCATIONS=(
  "1.3521,103.8198"
  "1.2844,103.8607"
  "1.3896,103.9988"
)

for loc in "${LOCATIONS[@]}"; do
  IFS=',' read lat lon <<< "$loc"
  python house_analyzer.py $lat $lon \
    --token "$ONEMAP_TOKEN" \
    --no-interactive \
    --format all
done
```

### Daily Analysis Automation

```bash
#!/bin/bash
# daily_analysis.sh

# Set token
export ONEMAP_TOKEN="your_token_here"

# Run analysis
python house_analyzer.py 1.3521 103.8198 \
  --all-themes \
  --no-interactive \
  --format all \
  --output "daily_reports/analysis_$(date +%Y%m%d)"

# Creates:
# daily_reports/analysis_20260211.json
# daily_reports/analysis_20260211.csv
# daily_reports/analysis_20260211.md
```

### Python Script Integration

```python
import subprocess
import json

# Run analyzer
result = subprocess.run([
    'python', 'house_analyzer.py',
    '1.3521', '103.8198',
    '--token', 'your_token',
    '--output', 'temp_analysis.json',
    '--no-interactive'
], capture_output=True)

# Load results
with open('temp_analysis.json') as f:
    data = json.load(f)

# Process data
print(f"Found {len(data['public_transport']['mrt_stations'])} MRT stations")
```

## Interactive Mode

If you don't use `--no-interactive`, the script will ask:

```
💾 Do you want to save the report? (y/n): y

Available formats:
  1. JSON (complete data structure)
  2. CSV (tabular format)
  3. Markdown (formatted report)
  4. All formats
Choose format (1-4, default=1): 2

Enter filename (or press Enter for auto-generated): my_report
```

This gives you flexibility to choose format after seeing the analysis.

## Tips & Best Practices

### 1. Use Timestamps for Version Control
```bash
# Auto-generated filenames include timestamps
--no-interactive
# Creates: house_analysis_1_3521_103_8198_20260211_092000.json
```

### 2. Save All Formats for Different Uses
```bash
--format all --output analysis
# Creates: analysis.json (for code), analysis.csv (for Excel), analysis.md (for docs)
```

### 3. Organize by Date
```bash
mkdir -p reports/$(date +%Y-%m)
python house_analyzer.py 1.3521 103.8198 --token "xxx" \
  --output "reports/$(date +%Y-%m)/report_$(date +%d)" \
  --no-interactive --format all
```

### 4. Use CSV for Quick Analysis
```bash
# Generate CSV, open in Excel for quick sorting
python house_analyzer.py 1.3521 103.8198 --token "xxx" \
  --output quick_analysis.csv --format csv --no-interactive

# Sort by distance in Excel to find nearest amenities
```

### 5. Use Markdown for Documentation
```bash
# Add to your project documentation
python house_analyzer.py 1.3521 103.8198 --token "xxx" \
  --output docs/location_analysis.md --format markdown --no-interactive
```

## Troubleshooting

### Error: "Permission denied"
```bash
# Check write permissions
ls -la /path/to/output/directory

# Use a writable directory
--output ~/reports/analysis.json
```

### Error: "File exists"
The script will overwrite existing files. To prevent accidental overwrites, use timestamps:
```bash
--output "analysis_$(date +%Y%m%d_%H%M%S).json"
```

### Large Files
JSON files can be large with `--all-themes`. Consider:
```bash
# Limit results
--max-results 5

# Or use CSV for smaller file size
--format csv
```

## Summary

| Format | Best Use | File Size | Compatibility |
|--------|----------|-----------|---------------|
| JSON | Programming, APIs | Large | All platforms |
| CSV | Spreadsheets, Analysis | Medium | Excel, Sheets, Numbers |
| Markdown | Documentation, Reports | Small | GitHub, Notion, Editors |

**Quick Commands:**
```bash
# Fastest: Auto-save JSON
python house_analyzer.py LAT LON --token "xxx" --no-interactive

# Best for Excel: Save CSV
python house_analyzer.py LAT LON --token "xxx" -o data.csv -f csv --no-interactive

# Best for docs: Save Markdown
python house_analyzer.py LAT LON --token "xxx" -o report.md -f md --no-interactive

# Save everything: All formats
python house_analyzer.py LAT LON --token "xxx" -o analysis -f all --no-interactive
```
