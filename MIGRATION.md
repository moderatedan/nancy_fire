# Migrating from v1 → v2

v2 is a full rebuild. The old repo has accumulated files that should NOT come
along. Here's the honest cleanup list.

## Delete these (junk / accidents)

| File | Why |
|---|---|
| `pd`, `tk`, `requests` | Accidental commits — these look like pip/console output redirected to files named after the imports |
| `python3 stock_tracker.py` | Misnamed (the command got baked into the filename) |
| `python3 stock_tracker (copy).py` | Duplicate of the above |
| `Recap of How to Get the Application to Work` | Extensionless notes file — its content now lives in README.md |
| `SimpleGUIApp.py`, `sprite_display.py` | Practice scripts superseded by the web dashboard |
| `transaction_data.py`, `transaction_data_processor.py`, `analyze_transactions.py`, `transaction_analyzer.py`, `stock_tracker.py`, `nancy_fire_app.py` | The v1 Tkinter app — replaced by `index.html` + `fetch_trades.py` |

## Keep / transform these

| File | Action |
|---|---|
| `8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png` | **Keep** — rename to `nancy.png` (`git mv '8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png' nancy.png`). The dashboard also recognizes the old filename as a fallback. |
| `8b8YFRSSshx4Sfy9fk9w--1--0j7p9.jpeg` | Keep one image; delete the duplicate format |
| `transaction_data.csv` | Optional keep — `fetch_trades.py --csv transaction_data.csv` can import it |
| `.gitignore` | Replace with the new one (adds `nancy_fire_env/`, pycache, editor files) |

## One-shot migration

```bash
cd nancy_fire
git rm 'pd' 'tk' 'requests' 'python3 stock_tracker.py' \
       'python3 stock_tracker (copy).py' \
       'Recap of How to Get the Application to Work' \
       SimpleGUIApp.py sprite_display.py transaction_data.py \
       transaction_data_processor.py analyze_transactions.py \
       transaction_analyzer.py stock_tracker.py nancy_fire_app.py \
       '8b8YFRSSshx4Sfy9fk9w--1--0j7p9.jpeg'
git mv '8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png' nancy.png

# copy in the v2 files (index.html, fetch_trades.py, data/, .github/, docs)
# then:
python3 fetch_trades.py
git add -A
git commit -m "v2: static dashboard, real disclosure data, zero deps, weekly auto-refresh"
git push
```

## Set the eye positions

Open `index.html`, top of the `<style>` block:

```css
--eye1-x: 42%; --eye1-y: 34%;
--eye2-x: 58%; --eye2-y: 34%;
```

Adjust until the glow dots sit over the eyes in your image. Two minutes, tops.
