# Swedish stock research dashboard

A read-only research dashboard for the Stockholm exchange (OMXS30): syncs
your real Avanza portfolio, charts price history, computes simple technical
signals (SMA/RSI/MACD), and includes a page of historical trader case
studies for context.

## What this app deliberately does NOT do

It never places, edits, or cancels a real order. `backend/app/avanza_client.py`
only calls read endpoints (`get_overview`, `get_accounts_positions`,
`search_for_stock`, `get_chart_data`, `get_market_data`). The Avanza library
also supports `place_order`, `place_stop_loss_order`, etc. - this app doesn't
import or call any of them. If you extend this into something that trades
automatically, that's a deliberate decision with real money at stake, worth
making on its own, not something to bolt on quietly.

## Important context before you connect a real account

- **Avanza has no official public API.** This app uses `avanza-api`, a
  community reverse-engineered client. It requires your real username,
  password, and TOTP secret, and Avanza can change or block the endpoints
  it depends on at any time without notice. Using it may be against
  Avanza's terms of service - that's your call to make, with full
  information.
- **Never commit your `.env` file.** It's already git-ignored. Don't put
  real credentials anywhere else in the repo (issues, commit messages,
  screenshots).
- **The technical signals are descriptive, not predictive.** SMA/RSI/MACD
  describe what a price series recently did. None of it guarantees future
  performance. This is not financial advice.

## Project structure

```
backend/    FastAPI app (Python) - portfolio sync, chart data, signal calc
frontend/   React + Vite dashboard (portfolio view, screener, trader case studies)
```

## Running it locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Leave DEMO_MODE=true to explore with fake portfolio data first.
# To use your real account, set DEMO_MODE=false and fill in
# AVANZA_USERNAME / AVANZA_PASSWORD / AVANZA_TOTP_SECRET.
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Then open the URL Vite prints (usually `http://localhost:5173`).

## Getting your Avanza TOTP secret

Avanza requires two-factor login. To get a TOTP secret you can put in
`.env`:

1. On avanza.se: Profile > Settings > Login and logout > Two-factor login.
2. Choose "another two-factor app" instead of scanning the QR code, and
   Avanza will show you the raw secret text - that's your
   `AVANZA_TOTP_SECRET`.

Keep this secret exactly as secret as your password.

## Publishing to GitHub

```bash
cd swe-stock-app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Double check `git status` shows no `.env` file staged before you commit -
it's git-ignored, but it's worth a second look before anything with real
credentials goes anywhere public.

## Extending it

- **Full market coverage:** `backend/app/tickers.py` has a starter OMXS30
  list, not all ~900 Stockholm-listed instruments. You can extend it
  manually, or wire up Avanza's inspiration-list / search endpoints to
  pull a fuller universe.
- **More indicators:** `backend/app/indicators.py` is a plain, readable
  place to add Bollinger Bands, ATR, volume-based signals, etc.
- **Deployment:** the backend is a standard FastAPI app (deployable to
  Render, Fly.io, Railway, etc.) and the frontend is a standard Vite app
  (deployable to Vercel, Netlify, or GitHub Pages with a build step).
