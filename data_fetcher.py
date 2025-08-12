# data_fetcher.py
import requests

OKX_BASE = "https://www.okx.com"

def fetch_data(inst_id="BTC-USDT-SWAP", sz=5):
    """
    Devuelve best_bid, best_ask, mid, spread_bp y top_depth_usd a partir del order book de OKX (top N).
    """
    url = f"{OKX_BASE}/api/v5/market/books"
    params = {"instId": inst_id, "sz": str(sz)}
    r = requests.get(url, params=params, timeout=6)
    r.raise_for_status()
    js = r.json()
    if js.get("code") != "0":
        raise RuntimeError(f"OKX error {js.get('code')}: {js.get('msg')}")
    d0 = (js.get("data") or [None])[0] or {}
    bids = d0.get("bids") or []
    asks = d0.get("asks") or []
    if not bids or not asks:
        raise RuntimeError("Libro vacío")

    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])
    mid = (best_bid + best_ask) / 2.0
    spread_bp = ((best_ask - best_bid) / mid) * 10000.0

    def sum_usd(levels, n=5):
        s = 0.0
        for i in range(min(n, len(levels))):
            p = float(levels[i][0]); q = float(levels[i][1])
            s += p * q
        return s

    bid_usd_top5 = sum_usd(bids, sz)
    ask_usd_top5 = sum_usd(asks, sz)
    top_depth_usd = min(bid_usd_top5, ask_usd_top5)

    return {
        "instId": inst_id,
        "best_bid": best_bid,
        "best_ask": best_ask,
        "mid": mid,
        "spread_bp": spread_bp,
        "bid_usd_top5": bid_usd_top5,
        "ask_usd_top5": ask_usd_top5,
        "top_depth_usd": top_depth_usd
    }
