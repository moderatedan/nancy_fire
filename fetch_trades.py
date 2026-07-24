#!/usr/bin/env python3
"""
fetch_trades.py — pull publicly disclosed congressional stock trades and
write data/trades.json for the Nancy Fire dashboard.

Sources (in order of preference):
  1. House Stock Watcher — a free, volunteer-maintained mirror of House
     STOCK Act periodic transaction reports, served as clean JSON from S3.
  2. A local CSV (--csv), for manual imports or when the mirror is down.

What this script does NOT do: scrape third-party tracker websites, invent
data, or call any API that requires an account. Disclosures are public
records; this just reshapes them.

Facts worth knowing about the data itself:
  * The STOCK Act gives members 45 days to disclose, so "real time" here
    means "as filed" — the dashboard shows the lag for every trade.
  * Amounts are reported as ranges (e.g. "$1,000,001 - $5,000,000"),
    never exact figures. We keep the range and also compute a midpoint
    for rough volume math, clearly labeled an estimate.
  * Rep. Pelosi's disclosed trades are typically executed by her spouse;
    the `owner` field from the filing is preserved.

Usage:
  python3 fetch_trades.py                          # default member: Pelosi
  python3 fetch_trades.py --member "Pelosi"        # any House member
  python3 fetch_trades.py --csv transaction_data.csv
  python3 fetch_trades.py --out data/trades.json --limit 500

License: MIT
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HOUSE_DATA_URL = ("https://house-stock-watcher-data.s3-us-west-2"
                  ".amazonaws.com/data/all_transactions.json")

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = BASE_DIR / "data" / "trades.json"

AMOUNT_RANGE_RE = re.compile(r"\$([\d,]+)\s*-\s*\$([\d,]+)")


# --------------------------------------------------------------------------- #
# Normalization
# --------------------------------------------------------------------------- #


def parse_date(raw: str) -> str | None:
    """Accept the formats seen in filings; return ISO YYYY-MM-DD or None."""
    raw = (raw or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def amount_midpoint(amount: str) -> int | None:
    """'$1,001 - $15,000' → 8000 (rough midpoint; an estimate, not a fact)."""
    m = AMOUNT_RANGE_RE.search(amount or "")
    if not m:
        return None
    lo = int(m.group(1).replace(",", ""))
    hi = int(m.group(2).replace(",", ""))
    return (lo + hi) // 2


def normalize_type(raw: str) -> str:
    raw = (raw or "").strip().lower()
    if "purchase" in raw or raw == "buy":
        return "buy"
    if "sale" in raw or raw == "sell":
        return "sell"
    if "exchange" in raw:
        return "exchange"
    return raw or "unknown"


def disclosure_lag_days(tx_date: str | None, disc_date: str | None) -> int | None:
    if not tx_date or not disc_date:
        return None
    try:
        t = datetime.strptime(tx_date, "%Y-%m-%d")
        d = datetime.strptime(disc_date, "%Y-%m-%d")
        return (d - t).days
    except ValueError:
        return None


def normalize_record(rec: dict) -> dict | None:
    """Map a House Stock Watcher record to the dashboard schema."""
    tx_date = parse_date(rec.get("transaction_date", ""))
    disc_date = parse_date(rec.get("disclosure_date", ""))
    if not tx_date:
        return None  # a handful of records carry unparseable dates; skip
    ticker = (rec.get("ticker") or "").strip()
    if ticker in ("--", "-", "N/A"):
        ticker = ""
    return {
        "transaction_date": tx_date,
        "disclosure_date": disc_date,
        "lag_days": disclosure_lag_days(tx_date, disc_date),
        "ticker": ticker,
        "asset": (rec.get("asset_description") or "").strip(),
        "type": normalize_type(rec.get("type", "")),
        "amount": (rec.get("amount") or "").strip(),
        "amount_mid": amount_midpoint(rec.get("amount", "")),
        "owner": (rec.get("owner") or "").strip(),
        "member": (rec.get("representative") or "").strip(),
        "source_link": (rec.get("ptr_link") or "").strip(),
    }


# --------------------------------------------------------------------------- #
# Sources
# --------------------------------------------------------------------------- #


def fetch_house_dataset() -> list[dict]:
    print(f"Fetching House disclosure dataset...\n  {HOUSE_DATA_URL}")
    req = urllib.request.Request(
        HOUSE_DATA_URL, headers={"User-Agent": "nancy-fire/2.0 (personal use)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(
            f"Could not reach the dataset ({exc}).\n"
            "The House Stock Watcher mirror is volunteer-run and can go "
            "stale or down. Options:\n"
            "  * try again later\n"
            "  * import a CSV instead:  python3 fetch_trades.py --csv file.csv\n"
            "  * see README → 'When the data source breaks' for alternatives")
    if not isinstance(data, list) or not data:
        sys.exit("Dataset downloaded but looks empty/unexpected — see README "
                 "→ 'When the data source breaks'.")
    print(f"  {len(data):,} total House transactions in dataset")
    return data


def read_csv(path: Path) -> list[dict]:
    """Import a CSV with (at least) transaction_date, ticker, type, amount.

    Also accepts the original nancy_fire transaction_data.csv — unknown
    columns are ignored, missing ones become blank.
    """
    if not path.exists():
        sys.exit(f"CSV not found: {path}")
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for raw in csv.DictReader(fh):
            # be forgiving about header names
            low = {k.strip().lower().replace(" ", "_"): (v or "")
                   for k, v in raw.items()}
            rows.append({
                "transaction_date": low.get("transaction_date")
                or low.get("date", ""),
                "disclosure_date": low.get("disclosure_date", ""),
                "ticker": low.get("ticker") or low.get("symbol", ""),
                "asset_description": low.get("asset_description")
                or low.get("asset") or low.get("description", ""),
                "type": low.get("type") or low.get("transaction_type", ""),
                "amount": low.get("amount", ""),
                "owner": low.get("owner", ""),
                "representative": low.get("representative")
                or low.get("member", ""),
                "ptr_link": low.get("ptr_link") or low.get("source_link", ""),
            })
    print(f"  {len(rows)} rows read from {path}")
    return rows


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> None:
    p = argparse.ArgumentParser(
        description="Build data/trades.json from public STOCK Act disclosures.")
    p.add_argument("--member", default="Pelosi",
                   help="filter: member name contains this (default: Pelosi). "
                        "Use --member '' for ALL members (big file).")
    p.add_argument("--csv", help="import from a local CSV instead of fetching")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="output path")
    p.add_argument("--limit", type=int, default=0,
                   help="keep only the N most recent trades (0 = all)")
    args = p.parse_args()

    raw = read_csv(Path(args.csv)) if args.csv else fetch_house_dataset()

    needle = args.member.strip().lower()
    normalized = []
    for rec in raw:
        n = normalize_record(rec)
        if n is None:
            continue
        if needle and needle not in n["member"].lower():
            continue
        normalized.append(n)

    if not normalized:
        sys.exit(f"No trades matched member filter '{args.member}'. "
                 "Check the spelling, or use --member '' for everyone.")

    normalized.sort(key=lambda r: r["transaction_date"], reverse=True)
    if args.limit:
        normalized = normalized[: args.limit]

    out = {
        "sample": False,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "member_filter": args.member,
        "source": ("local CSV import" if args.csv
                   else "House Stock Watcher (house-stock-watcher-data S3)"),
        "count": len(normalized),
        "trades": normalized,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    buys = sum(1 for t in normalized if t["type"] == "buy")
    sells = sum(1 for t in normalized if t["type"] == "sell")
    print(f"\nWrote {out_path}: {len(normalized)} trades "
          f"({buys} buys / {sells} sells) for filter '{args.member}'.")
    print("Open index.html — the dashboard reads this file automatically.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
