# app.py
from flask import Flask, jsonify, request
import data_fetcher

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"ok": True})

@app.route("/data", methods=["GET"])
def get_data():
    inst = request.args.get("instId", "BTC-USDT-SWAP")
    sz = int(request.args.get("sz", "5"))
    try:
        data = data_fetcher.fetch_data(inst_id=inst, sz=sz)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
