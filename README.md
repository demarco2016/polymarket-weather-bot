# Polymarket Weather Bot

Self-calibrating weather-trading bot for Polymarket.

## Features
- Trades on 20 cities across 4 continents
- 3 forecast sources: ECMWF, HRRR, METAR
- EV+ automatic calculation
- Kelly Criterion position sizing
- Self-calibration every 30 forecasts per city
- Full data storage (forecast, trade, resolution)

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## How it works
1. Fetches forecasts from Open-Meteo API (3 sources)
2. Compares to actual station data
3. Calculates +EV opportunities
4. Sizes positions using Kelly Criterion
5. Snaps all trade data
6. Auto-calibrates every 30 forecasts
