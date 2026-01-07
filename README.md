# Data Ireland Housing Analysis

Data analysis project that collects, processes, and analyzes Irish housing rent data from the Central Statistics Office (CSO) to identify trends and patterns in the rental market.

## Overview

This project retrieves housing rent data from Ireland's Central Statistics Office (CSO) public APIs, enriches it with geographic coordinates and census data, and exports the processed dataset for visualization and analysis.

## Features

- **Data Collection**: Fetches rent and census data from CSO APIs
- **Geocoding**: Adds geographic coordinates using Nominatim/OpenStreetMap
- **Data Enrichment**: Joins rent data with census demographics
- **Data Cleaning**: Standardizes and validates data quality
- **Export**: Outputs processed data to CSV and Google Sheets

## Tech Stack

- **Python** - Data processing
- **Pandas** - Data manipulation and analysis
- **Geopy** - Geocoding addresses to coordinates
- **Requests** - API data retrieval
- **Google APIs** - Export to Google Sheets

## Project Structure

```
data-ireland-housing-analysis/
├── MainHouseCso.py              # Main entry point
├── Modules/
│   ├── ModuleImportData.py      # CSO API data retrieval
│   ├── ModuleCleanData.py       # Data cleaning functions
│   ├── ModuleGetLocation.py     # Geocoding utilities
│   ├── ModuleExportData.py      # Export to CSV/Google Sheets
│   └── google_apis.py           # Google Sheets integration
├── Sources/                      # Source data files
├── output/                       # Processed output files
├── TestModulesSection/          # Module tests
└── QC_Dashboard_qc_list.ipynb   # Quality control notebook
```

## Data Sources

- **CSO Rent Data**: [data.cso.ie](https://data.cso.ie/) - Irish rental market statistics
- **CSO Census Data**: Population and demographic data by county
- **OpenStreetMap**: Geographic coordinates via Nominatim

## Pipeline Steps

1. **Import**: Fetch rent and census data from CSO APIs
2. **Clean**: Standardize column names, handle missing values
3. **Geocode**: Add latitude/longitude coordinates by location
4. **Join**: Merge rent data with census demographics
5. **Export**: Save to CSV and optionally to Google Sheets

## Usage

```bash
# Run the main analysis pipeline
python MainHouseCso.py
```

## Output

The pipeline generates:
- `output/data_cso_ie_rent_out.csv` - Processed rent data with coordinates and census info

## Analysis Opportunities

- Rent price trends by county over time
- Correlation between rent prices and population density
- Geographic visualization of rental hotspots
- Year-over-year rent growth analysis

## License

MIT
