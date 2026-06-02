import time
from bot.forecast import get_forecasts, get_station_data
from bot.kelly import calculate_ev
from bot.trading import auto_size
from bot.calibrate import snapshot_trade, calibrate
from bot.polymarket import find_market_for_city, get_market_price, place_trade
from config import CITIES, MIN_EV, KELLY_FRACTION, CALIBRATION_INTERVAL

forecast_history = {city: [] for city in CITIES}

def run_bot():
    print(f"Polymarket weather bot | Mode: LIVE | Min EV: {MIN_EV}")
    for city in CITIES:
        print(f"\n--- {city} ---")
        forecasts = get_forecasts(city)
        actual = get_station_data(city)
        if actual is None:
            continue

        market = find_market_for_city(city)
        if not market:
            print(f"  No weather market found for {city}")
            continue

        token_id = market["token_ids"][0] if market["token_ids"] else None
        if not token_id:
            print(f"  No token ID for {city} market")
            continue

        bid, ask, _ = get_market_price(token_id)
        if bid is None and ask is None:
            print(f"  No price data for {city}")
            continue

        print(f"  Market: {market['question']}")
        print(f"  Price: bid={bid}, ask={ask}")

        for source, forecast_temp in forecasts.items():
            if forecast_temp is None:
                continue
            market_prob = ask if ask else 0.5
            ev, prob = calculate_ev(forecast_temp, market_prob, actual)
            if ev > MIN_EV:
                size = auto_size(ev)
                if size > 0:
                    side = "BUY" if ev > 0 else "SELL"
                    price = round(ask if side == "BUY" else bid, 2) if (ask and bid) else 0.5
                    print(f"  Placing {side} {size} shares @ {price} | EV={ev:.3f}")
                    result = place_trade(token_id, side, price, size)
                    if result and result.get("order"):
                        print(f"  Order placed: {result['order']['id']}")
                    snapshot_trade(city, {source: forecast_temp}, size, ev, result)
                else:
                    print(f"  EV={ev:.3f} but size=0")
            else:
                print(f"  {source}: EV={ev:.3f} (below MIN_EV)")

        forecast_history[city].append({
            "forecasts": forecasts,
            "actual": actual,
            "timestamp": time.time(),
        })
        if len(forecast_history[city]) >= CALIBRATION_INTERVAL:
            new_min_ev = calibrate(forecast_history[city])
            print(f"  Calibrated MIN_EV -> {new_min_ev:.4f}")
            forecast_history[city] = []

if __name__ == "__main__":
    run_bot()
