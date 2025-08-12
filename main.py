from fastapi import FastAPI, Query
from typing import Optional
import time

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ob-lite")
def ob_lite(instId: str, sz: int = 5):
    return {
        "instId": instId,
        "best_bid": 120047.5,
        "best_ask": 120047.6,
        "mid": (120047.5 + 120047.6) / 2,
        "spread_bp": (120047.6 - 120047.5) / 120047.5 * 10000,
        "top_depth_usd": 500000
    }

@app.get("/levels")
def levels(instId: str):
    return {
        "instId": instId,
        "PDH": 121000,
        "PDL": 119000,
        "VWAP": 120100,
        "VWAP_upper": 120200,
        "VWAP_lower": 120000
    }

@app.get("/timebox")
def timebox():
    now = int(time.time())
    remaining = 900 - (now % 900)
    return {
        "minutes_remaining": remaining // 60,
        "seconds_remaining": remaining % 60
    }

@app.get("/assemble")
def assemble(instId: str, size: float, leverage: int, fee_entry: float, fee_exit: float):
    ob = ob_lite(instId)
    lv = levels(instId)
    tb = timebox()
    cost_est = size * ob["mid"] / leverage
    return {
        "ob": ob,
        "levels": lv,
        "timebox": tb,
        "cost_est": cost_est,
        "fees": {
            "entry_fee": size * ob["mid"] * fee_entry,
            "exit_fee": size * ob["mid"] * fee_exit
        }
    }
