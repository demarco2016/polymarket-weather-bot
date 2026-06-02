import json
import os
from datetime import datetime

TRADE_LOG = os.path.join(os.path.dirname(__file__), "..", "data", "trades.json")

def snapshot_trade(city, forecast, size, ev, resolution=None):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "city": city,
        "forecast": forecast,
        "size": size,
        "ev": ev,
        "resolution": resolution,
    }
    trades = []
    if os.path.exists(TRADE_LOG):
        with open(TRADE_LOG, "r") as f:
            trades = json.load(f)
    trades.append(record)
    with open(TRADE_LOG, "w") as f:
        json.dump(trades, f, indent=2)
    return record

def calibrate(forecasts_data):
    errors = []
    for f in forecasts_data:
        if f["actual"] is not None and f["forecast"] is not None:
            errors.append(abs(f["actual"] - f["forecast"]))
    if len(errors) < 5:
        return 0.05
    mean_error = sum(errors) / len(errors)
    return min(mean_error * 0.1, 0.15)
