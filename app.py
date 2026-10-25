import os
import requests
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
GECKO = "https://api.geckoterminal.com/api/v2"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status":"ok","app":"Advanced Crypto Analysis Platform"})

@app.get("/api/solana/trending")
def trending():
    try:
        r=requests.get(f"{GECKO}/networks/solana/trending_pools", timeout=15, headers={"Accept":"application/json"})
        r.raise_for_status()
        out=[]
        for item in r.json().get("data",[])[:20]:
            a=item.get("attributes",{})
            out.append({"pool":a.get("name"),"address":a.get("address"),"price_usd":a.get("base_token_price_usd"),
              "volume_24h":(a.get("volume_usd") or {}).get("h24"),"price_change_24h":(a.get("price_change_percentage") or {}).get("h24"),
              "reserve_usd":a.get("reserve_in_usd"),"network":"solana"})
        return jsonify({"data":out,"source":"GeckoTerminal"})
    except Exception as e:
        return jsonify({"error":"Market data is temporarily unavailable.","detail":str(e)[:160]}),502

@app.get("/api/solana/pools/<path:pool_address>/ohlcv")
def ohlcv(pool_address):
    timeframe=request.args.get("timeframe","hour")
    if timeframe not in {"minute","hour","day"}: timeframe="hour"
    aggregate=request.args.get("aggregate","1")
    if aggregate not in {"1","4","12","24"}: aggregate="1"
    try:
        r=requests.get(f"{GECKO}/networks/solana/pools/{pool_address}/ohlcv/{timeframe}",
          params={"aggregate":aggregate,"limit":100,"currency":"usd"},timeout=15,headers={"Accept":"application/json"})
        r.raise_for_status()
        rows=r.json().get("data",{}).get("attributes",{}).get("ohlcv_list",[])
        candles=[{"time":x[0],"open":x[1],"high":x[2],"low":x[3],"close":x[4],"volume":x[5]} for x in rows if isinstance(x,list) and len(x)>=6]
        return jsonify({"data":list(reversed(candles)),"source":"GeckoTerminal"})
    except Exception as e:
        return jsonify({"error":"Historical candles are temporarily unavailable.","detail":str(e)[:160]}),502

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
