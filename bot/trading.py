MIN_EV = 0.05
KELLY_FRACTION = 0.25
BANKROLL = 1000.0

def auto_size(ev, bankroll=BANKROLL):
    if ev <= MIN_EV:
        return 0.0
    base = bankroll * KELLY_FRACTION
    size = base * (ev / 0.1)
    return round(min(size, bankroll * 0.1), 2)
