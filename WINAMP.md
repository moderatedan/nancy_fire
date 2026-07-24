# 🎵 Nancy Fire Amp — the Winamp skin

A second front-end for the same data: `winamp.html` renders the disclosure
feed as a classic late-90s media player, and a ~90-line WebKitGTK launcher
turns it into a real Linux desktop app. No Electron, no Node — the only
dependencies are distro packages.

## The metaphor

| Winamp | Nancy Fire Amp |
|---|---|
| Now-playing marquee | The currently selected filing, scrolling in LCD green |
| Big time digits | **Days between trade and filing** (turns red past the 45-day STOCK Act window) |
| Playlist | The disclosure log — click any row to load it |
| ▶ Play | Auto-advance through filings ("the reel"); speed slider = seconds per filing |
| ⏮ ⏭ 🔀 | Previous / next / shuffle filings (also ← → and spacebar) |
| Spectrum analyzer | Animated bars whose energy scales with the current filing's estimated size |
| kbps / kHz slots | BUY % · track count · est. volume · top ticker |
| Album art | The mascot — ember glow + eye flicker when buy volume ≥ 60%, smoke on buys and clicks |
| Ticker tape | Last ten filings with ▲/▼ |

Everything reads the same `data/trades.json` as the main dashboard, with the
same rule: until you run `fetch_trades.py`, it plays **clearly-labeled
fictional demo data** and blinks DEMO in the LCD.

## Run it in a browser (works everywhere)

```bash
python3 fetch_trades.py          # optional — demo data otherwise
python3 -m http.server 8080
# → http://localhost:8080/winamp.html
```

## Run it as a native Linux app

```bash
# Debian/Ubuntu
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.1
# Fedora:  sudo dnf install python3-gobject gtk3 webkit2gtk4.1
# Arch:    sudo pacman -S python-gobject gtk3 webkit2gtk-4.1

python3 desktop/nancy_fire_desktop.py                 # winamp skin
python3 desktop/nancy_fire_desktop.py --page index.html   # full dashboard
```

The window is undecorated — drag it by the skin's own gold title bar; `_`
minimizes, `X` closes (Esc also closes, F11 toggles fullscreen). The title
bar buttons talk to GTK through a WebKit message bridge and degrade
gracefully in a plain browser.

## Install into the app menu (optional)

```bash
sudo mkdir -p /opt/nancy_fire
sudo cp -r . /opt/nancy_fire
sudo cp desktop/nancy-fire.desktop /usr/share/applications/
```

(Or keep it per-user: copy the .desktop file to
`~/.local/share/applications/` and edit `Exec=`/`Path=` to your clone path.)

## Notes

- **Fonts:** the skin uses the Silkscreen pixel font from Google Fonts and
  falls back to monospace offline. Vendor the woff2 locally for a fully
  offline build.
- **Eye positions:** same CSS variables as the main dashboard —
  `--eye1-x/y`, `--eye2-x/y` near the top of `winamp.html`.
- **Reduced motion:** all animation respects `prefers-reduced-motion`.
- Same data honesty applies: filings lag up to 45 days, amounts are ranges,
  and none of this is financial advice. It's a public-records viewer that
  really whips the llama's... filings.
