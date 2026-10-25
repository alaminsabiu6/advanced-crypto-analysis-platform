# Advanced Crypto Analysis Platform — Starter

This is a separate project and does not change your existing Solana Gem Scanner.

## Included
- Solana trending pools from GeckoTerminal's public API
- Historical OHLCV candle API
- Candlestick/volume chart
- Browser-side EMA 20/50, RSI 14, MACD, and approximate recent support/resistance
- Simple/advanced view and timeframe selection
- Health endpoint at `/health`

## Not included yet
AI commentary, whale tracking, alerts, wallet connections, or trade execution. These should be added in later stages after the core app is tested.

## Run locally
`pip install -r requirements.txt`
`python app.py`
Then open `http://localhost:10000`.

## Deploy
Create a **new GitHub repository** named `advanced-crypto-analysis-platform`, upload the contents of this folder there, and create a **new Render Web Service** from that repository. Do not connect this project to the existing scanner repository.

Data comes from GeckoTerminal's public API and may be rate-limited or incomplete. Indicators are informational, not guarantees or financial advice.
