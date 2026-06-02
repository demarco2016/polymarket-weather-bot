import requests
import time
from config import (
    CLOB_HOST, CHAIN_ID, PRIVATE_KEY,
    CLOB_API_KEY, CLOB_API_SECRET, CLOB_API_PASSPHRASE,
    FUNDER_ADDRESS, SIGNATURE_TYPE, BUILDER_CODE,
)
from py_clob_client_v2 import (
    ClobClient, ApiCreds, OrderArgs, OrderType,
    PartialCreateOrderOptions, Side, BuilderConfig,
)

_client = None

def get_client():
    global _client
    if _client is not None:
        return _client
    kwargs = dict(
        host=CLOB_HOST,
        chain_id=CHAIN_ID,
        key=PRIVATE_KEY,
    )
    if FUNDER_ADDRESS:
        kwargs["funder"] = FUNDER_ADDRESS
    if SIGNATURE_TYPE:
        kwargs["signature_type"] = SIGNATURE_TYPE
    if BUILDER_CODE:
        kwargs["builder_config"] = BuilderConfig(builder_code=BUILDER_CODE)

    _client = ClobClient(**kwargs)

    if CLOB_API_KEY and CLOB_API_SECRET and CLOB_API_PASSPHRASE:
        _client.set_api_creds(ApiCreds(
            api_key=CLOB_API_KEY,
            api_secret=CLOB_API_SECRET,
            api_passphrase=CLOB_API_PASSPHRASE,
        ))
    else:
        creds = _client.create_or_derive_api_key()
        print("[Polymarket] API creds derived. Save them:")
        print(f"  CLOB_API_KEY={creds.api_key}")
        print(f"  CLOB_API_SECRET={creds.api_secret}")
        print(f"  CLOB_API_PASSPHRASE={creds.api_passphrase}")
        _client.set_api_creds(creds)
    return _client


def find_weather_markets(limit=10):
    url = "https://gamma-api.polymarket.com/markets"
    params = dict(closed=False, limit=limit, tag="weather", order="volume", ascending=False)
    try:
        resp = requests.get(url, params=params, timeout=10)
        markets = resp.json()
        result = []
        for m in markets:
            result.append({
                "id": m["id"],
                "question": m["question"],
                "condition_id": m.get("conditionId"),
                "token_ids": m.get("clobTokenIds", []),
                "outcome_prices": m.get("outcomePrices", []),
                "volume": m.get("volume", 0),
                "end_date": m.get("endDate"),
            })
        return result
    except Exception as e:
        print(f"[Gamma] Error fetching weather markets: {e}")
        return []


def find_market_for_city(city):
    markets = find_weather_markets(limit=50)
    for m in markets:
        if city.lower() in m["question"].lower():
            return m
    return None


def get_market_price(token_id):
    client = get_client()
    try:
        book = client.get_order_book(token_id)
        if book.get("asks"):
            best_ask = float(book["asks"][0]["price"])
        else:
            best_ask = None
        if book.get("bids"):
            best_bid = float(book["bids"][0]["price"])
        else:
            best_bid = None
        return best_bid, best_ask, book
    except Exception as e:
        print(f"[CLOB] Error fetching price: {e}")
        return None, None, None


def place_trade(token_id, side, price, size):
    client = get_client()
    order = OrderArgs(
        token_id=token_id,
        price=price,
        size=size,
        side=Side.BUY if side == "BUY" else Side.SELL,
    )
    try:
        resp = client.create_and_post_order(
            order_args=order,
            options=PartialCreateOrderOptions(tick_size="0.01"),
            order_type=OrderType.GTC,
        )
        return resp
    except Exception as e:
        print(f"[CLOB] Error placing order: {e}")
        return None


def get_balance():
    client = get_client()
    try:
        allowance = client.get_balance_allowance()
        return allowance
    except Exception as e:
        print(f"[CLOB] Error fetching balance: {e}")
        return None
