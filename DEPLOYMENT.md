# Deploying Nancy Fire v2

## GitHub Pages + weekly auto-refresh (the point of v2)

1. Push the migrated repo (see MIGRATION.md), including `.github/workflows/`.
2. **Settings → Pages → Source: Deploy from a branch → master / (root)**.
3. **Settings → Actions → General → Workflow permissions → "Read and write
   permissions"** — the update workflow commits `data/trades.json`.
4. Test the pipeline: **Actions → Update disclosure data → Run workflow**.
   Within a couple of minutes you should see a bot commit and the live site
   refresh at `https://moderatedan.github.io/nancy_fire/`.

After that it maintains itself: every Monday the Action pulls new filings,
commits only if something changed, and Pages redeploys.

## Local-only (fully private)

```bash
python3 fetch_trades.py
python3 -m http.server 8080
```

Nothing leaves your machine except the one request to the public dataset.

## Repo settings

- **Topics:** `congress`, `stock-act`, `transparency`, `dashboard`,
  `github-pages`, `open-data`, `python`
- **About:** "Self-hosted dashboard for publicly disclosed congressional
  stock trades. Static, zero deps, weekly auto-refresh. Not financial advice."

## Post-deploy checklist

- [ ] Run MIGRATION.md cleanup (the junk files are the #1 thing to fix)
- [ ] `mv` your mascot image to nancy.png and tune the eye positions
- [ ] Run the Action manually once and confirm the bot commit
- [ ] Confirm the DEMO banner disappears once real data is present
- [ ] Screenshots for docs/ (dashboard, bull-run glow, table)
- [ ] Tag it: `git tag v2.0.0 && git push --tags`
