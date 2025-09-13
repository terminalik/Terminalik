from textual.app import ComposeResult, App
from textual.containers import VerticalScroll
from textual.widgets import Markdown

import os
import threading
import requests

README_URL = "https://raw.githubusercontent.com/terminalik/TerminalikSSH/main/README.md"


def fetch_readme(url: str) -> str:
    # Prefer local README if exists
    for name in ("README.md", "readme.md"):
        if os.path.exists(name):
            try:
                with open(name, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"Failed to load README (\n{e}\n)"


class ReadmeMarkdown(VerticalScroll):
    def compose(self) -> ComposeResult:
        # Show placeholder and load in background
        yield Markdown("Loading README...", id="md")

    def on_mount(self) -> None:
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self) -> None:
        text = fetch_readme(README_URL)

        def _update() -> None:
            self.query_one("#md", Markdown).update(text)

        try:
            self.app.call_from_thread(_update)
        except Exception:
            _update()


if __name__ == "__main__":
    class _ReadmeApp(App):
        def compose(self) -> ComposeResult:
            yield ReadmeMarkdown()

    _ReadmeApp().run()
