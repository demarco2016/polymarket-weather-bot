def kelly_criterion(prob_win, odds):
    if prob_win <= 0 or prob_win >= 1:
        return 0
    b = odds - 1
    if b <= 0:
        return 0
    f_star = (prob_win * b - (1 - prob_win)) / b
    return max(f_star, 0)

def calculate_ev(forecast_temp, market_prob, strike_temp):
    forecast_error = abs(forecast_temp - strike_temp)
    confidence = max(0, 1 - (forecast_error / 10))
    estimated_prob = 0.5 + (confidence / 2)
    ev = estimated_prob - market_prob
    return ev, estimated_prob
