#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import webbrowser
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk, Gtk, WebKit2  # noqa: E402


class NancyFireWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Nancy Fire Amp")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Set up the WebKit view
        self.webview = WebKit2.WebView()
        self.webview.set_zoom_level(1.0)
        
        # Load the Winamp HTML
        html_path = Path(__file__).parent.parent / "winamp.html"
        if html_path.exists():
            self.webview.load_uri(f"file://{html_path}")
        else:
            # Fallback to demo mode
            self.webview.load_html("<h1>Nancy Fire Amp</h1><p>winamp.html not found</p>")
        
        # Add the webview to the window
        self.add(self.webview)
        
        # Connect signals
        self.connect("destroy", Gtk.main_quit)
        self.webview.connect("decide-policy", self.on_decide_policy)
        
        # Show everything
        self.show_all()
    
    def on_decide_policy(self, webview, decision, decision_type):
        # Handle external links
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            uri = decision.get_navigation_action().get_request().get_uri()
            if uri.startswith("http"):
                webbrowser.open(uri)
                decision.skip()
                return True
        return False


def main():
    # Ensure the data directory exists
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Create demo trades.json if it doesn't exist
    trades_file = data_dir / "trades.json"
    if not trades_file.exists():
        demo_data = {
            "trades": [
                {"date": "2026-07-06", "ticker": "NVDA", "type": "BUY", "amount": "1000001-5000000", "owner": "Spouse", "filed": "2026-07-18"},
                {"date": "2026-07-06", "ticker": "MSFT", "type": "BUY", "amount": "250001-500000", "owner": "Spouse", "filed": "2026-07-18"},
                {"date": "2026-06-10", "ticker": "AAPL", "type": "SELL", "amount": "500001-1000000", "owner": "Spouse", "filed": "2026-07-18"},
                {"date": "2026-05-28", "ticker": "AVGO", "type": "BUY", "amount": "100001-250000", "owner": "Spouse", "filed": "2026-07-18"},
            ]
        }
        with open(trades_file, "w") as f:
            json.dump(demo_data, f, indent=2)
        print("✅ Created demo trades.json")
    
    # Run the application
    win = NancyFireWindow()
    Gtk.main()


if __name__ == "__main__":
    main()
