from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.message import Message
from textual.widgets import (
    Input,
    Button,
    Label,
    Select,
    SelectionList,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.setups.setupDjango import setup_django
from utils.setups.setupVue import setup_vue
from utils.setups.setupDocker import setup_docker

class ProjectSetupForm(VerticalScroll):
    class Submitted(Message):
        def __init__(self, data: Dict[str, Any]) -> None:
            self.data = data
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Project Name:")
        # Force name to current directory and make it read-only
        yield Input(
            placeholder="Project folder name",
            value=os.path.basename(os.getcwd()),
            id="project_name",
            disabled=False,
        )
        yield Label("Frontend Framework:")
        options=["Vue", "React", "Svelte", "None"]
        yield Select(options=[(opt, opt.lower()) for opt in options], id="frontend_framework")
        yield Label("Backend Framework:")
        options=["Django", "Flask", "FastAPI", "None"]
        yield Select(options=[(opt, opt.lower()) for opt in options], id="backend_framework")
        yield Label("Include Options:")
        yield SelectionList(
            ("Docker", 0),
            ("Unfold", 1),
            id="include_options",
        )
        with Horizontal(id="buttons"):
            yield Button("Submit", id="submit", variant="success")
            yield Button("Cancel", id="cancel", variant="warning")



    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.post_message(self.Submitted(self._values()))
        elif event.button.id == "cancel":
            self.app.exit()
            # TODO: Back to main page

    def _values(self) -> Dict[str, Any]:
        """Collect normalized values for setups.

        Project name is always the current directory.
        """
        cwd = os.getcwd()
        name_input = self.query_one("#project_name", Input).value.strip()
        project_name = name_input or os.path.basename(cwd)
        frontend = self.query_one("#frontend_framework", Select).value
        backend = self.query_one("#backend_framework", Select).value
        sel_widget = self.query_one("#include_options", SelectionList)
        # SelectionList.selected may be a list of values or Selection objects depending on Textual version
        try:
            selected = {getattr(item, "id") for item in sel_widget.selected}  # type: ignore[attr-defined]
        except Exception:
            try:
                selected = set(sel_widget.selected)
            except Exception:
                selected = set()

        return {
            "project_name": project_name,
            "frontend_framework": frontend,
            "backend_framework": backend,
            "include_docker": 0 in selected,
            "include_unfold": 1 in selected,
        }