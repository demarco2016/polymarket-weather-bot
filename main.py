import json
import os
import time
from bot.forecast import get_forecasts, get_station_data
from bot.kelly import calculate_ev
from bot.trading import auto_size
from bot.calibrate import snapshot_trade, calibrate
from config import CITIES, SIMULATION_BANKROLL, MIN_EV, CALIBRATION_INTERVAL

forecast_history = {city: [] for city in CITIES}
bankroll = SIMULATION_BANKROLL

def run_bot():
    global bankroll
    print(f"Starting Polymarket weather bot | Bankroll: ${bankroll}")
    for city in CITIES:
        print(f"\n--- {city} ---")
        forecasts = get_forecasts(city)
        actual = get_station_data(city)
        if actual is None:
            continue
        for source, forecast_temp in forecasts.items():
            if forecast_temp is None:
                continue
            ev, prob = calculate_ev(forecast_temp, 0.5, actual)
            if ev > MIN_EV:
                size = auto_size(ev, bankroll)
                if size > 0:
                    print(f"  +EV trade on {source}: EV={ev:.3f}, size=${size}")
                    snapshot_trade(city, {source: forecast_temp}, size, ev)
                    bankroll -= size
                else:
                    print(f"  EV={ev:.3f} but size=0 (bankroll too low)")
            else:
                print(f"  {source}: EV={ev:.3f} (below MIN_EV)")
        forecast_history[city].append({
            "forecasts": forecasts,
            "actual": actual,
            "timestamp": time.time()
        })
        if len(forecast_history[city]) >= CALIBRATION_INTERVAL:
            new_min_ev = calibrate(forecast_history[city])
            print(f"  Calibrated MIN_EV -> {new_min_ev:.4f}")
            forecast_history[city] = []
    print(f"\nFinal bankroll: ${bankroll:.2f}")

if __name__ == "__main__":
    run_bot()
