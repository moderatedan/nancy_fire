# 🔥 Nancy Fire v2

> A personal, static, tracker-free dashboard for publicly disclosed congressional stock trades — glowing eyes and all.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)
![Data](https://img.shields.io/badge/data-public%20STOCK%20Act%20filings-blue.svg)
![Hosting](https://img.shields.io/badge/hosting-GitHub%20Pages-orange.svg)

Members of Congress must publicly disclose their stock trades under the STOCK Act. Nancy Fire turns those filings into a dashboard you host yourself: no accounts, no third-party trackers profiting from your attention, no backend — just a static page, a JSON file, and a Python script that refreshes it. Filter any House member; the default follows the most famous portfolio in Washington.

And yes: when disclosure momentum runs bullish, the eyes glow and the smoke rolls. Click the mascot for a burst. Serious data, unserious mascot.

---

## ✨ What's new in v2 (vs. the original Tkinter app)

| v1 | v2 |
|---|---|
| Tkinter desktop app, blocking scrape at startup | Static web dashboard, deploys to GitHub Pages |
| Scraped a third-party tracker site (2 columns) | Normalizes actual STOCK Act filing data (10 fields incl. amounts, owner, filing links) |
| 5 pip dependencies | **Zero** dependencies (stdlib fetcher + vanilla JS) |
| Manual refresh | GitHub Action refreshes data weekly, auto-commits |
| Static image tab | Ember-glow mascot, eye glow on bull runs, canvas smoke particles, click interactions |
| Quantity histogram | Momentum gauge, monthly buy/sell volume chart, filterable table, late-filing flags |

## 📸 Screenshots

> _Add yours (the mascot image isn't in this rebuild — see step 2 below):_

| Dashboard | Bull-run mode | Trades table |
|---|---|---|
| ![Dashboard](docs/screenshot-dashboard.png) | ![Bull run](docs/screenshot-bullrun.png) | ![Table](docs/screenshot-table.png) |

## 🚀 Setup

```bash
git clone https://github.com/moderatedan/nancy_fire.git
cd nancy_fire

# 1. Pull real disclosure data (writes data/trades.json)
python3 fetch_trades.py                      # default filter: Pelosi
# python3 fetch_trades.py --member "Greene"  # any House member
# python3 fetch_trades.py --member ""        # everyone (big)

# 2. Add the mascot: keep your original image and rename it
mv 8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png nancy.png   # (old filename also works)

# 3. Open it
python3 -m http.server 8080     # → http://localhost:8080
```

Until you run the fetcher, the page shows **clearly-labeled fictional demo data** (member "J. Sample (DEMO)") so the layout works out of the box — a banner reminds you it's not real.

## 🧠 Features

- **Momentum gauge** — trailing-90-day estimated buy vs. sell volume from filings. When buying dominates (≥60%), the mascot goes hot: pulsing ember glow, flickering eyes, ambient smoke.
- **Monthly activity chart** — buys up in green, sells down in red, estimated dollar volume by month (hand-rolled SVG, no chart library).
- **Filterable trade table** — every filing with ticker, asset, filed amount **range**, owner as filed, a link to the source PTR where available, and a **"filed after" column that flags filings past the 45-day STOCK Act window** ⚠.
- **Stats row** — trade counts, buy/sell split, estimated volume, most-traded ticker.
- **Auto-refresh CI** — `.github/workflows/update-data.yml` re-runs the fetcher every Monday and commits new filings; GitHub Pages redeploys itself.
- **Interactions** — click the mascot for a smoke burst (with a counter, because why not). `prefers-reduced-motion` disables all animation.
- **Eye positioning** — the glow dots are CSS variables; tune `--eye1-x/y` and `--eye2-x/y` at the top of `index.html` to your image in ~30 seconds.

## 📊 About the data (read this part)

- **Source:** public STOCK Act periodic transaction reports, via the volunteer-run [House Stock Watcher](https://housestockwatcher.com) JSON mirror. Public records, reshaped — nothing scraped from commercial trackers.
- **It is not real-time.** Members have **45 days** to file, so every number here lags reality. The dashboard prints this on the page rather than pretending otherwise.
- **Amounts are ranges.** Filings report brackets like "$1,000,001 – $5,000,000", never exact figures. Volume stats use range midpoints and are labeled estimates.
- **Owner matters.** Filings often list a spouse or dependent as the transacting owner (famously so for the default member); the owner column preserves exactly what was filed.
- **Not financial advice.** This is a public-records viewer with a cartoon on it.

### When the data source breaks

The mirror is volunteer-maintained. If `fetch_trades.py` fails:
1. Try again later, or import manually: `python3 fetch_trades.py --csv your_file.csv` (accepts the old `transaction_data.csv` format too).
2. Alternative sources to adapt: the House Clerk's Financial Disclosure portal (official, PDFs), or a commercial API (e.g., Financial Modeling Prep's House disclosures endpoint) — PRs adding a second source welcome.

## 🎵 Bonus: the Winamp skin

`winamp.html` renders the same data as a classic late-90s media player — playlist of filings, LCD marquee, spectrum analyzer driven by trade size, transport controls — and `desktop/nancy_fire_desktop.py` (~90 lines of WebKitGTK, no Electron) runs it as a native Linux desktop app with the skin's own draggable title bar. See [WINAMP.md](WINAMP.md).

## 🗺️ Roadmap

- [ ] Senate support (senate-stock-watcher dataset, same shape)
- [ ] Price overlay: trade markers on the ticker's chart
- [ ] Multi-member comparison view
- [ ] RSS/JSON feed of new filings from the CI run

## 📄 License

[MIT](LICENSE). Disclosure data is public record.
