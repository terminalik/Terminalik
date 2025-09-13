from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Static,
    Label,
    RichLog,
)
from textual.screen import Screen
import threading

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.setups.setupDjango import setup_django
from utils.setups.setupVue import setup_vue
from utils.setups.setupDocker import setup_docker
from components.projectSetupForm import ProjectSetupForm

class ProjectSetupPane(VerticalScroll):
    """A non-Screen widget version suitable for Tab panes in the main app."""

    def compose(self) -> ComposeResult:
        yield Label("Terminalik Project Setup", id="title")
        with VerticalScroll(id="form_container"):
            yield ProjectSetupForm()
        yield Label("Output", id="output_title")
        # Scrollable log box
        yield RichLog(highlight=False, markup=False, wrap=False, id="output_log")

    def on_mount(self) -> None:
        self._output_lines: list[str] = []

    def log_line(self, text: str) -> None:
        out = self.query_one("#output_log", RichLog)
        # Write line and keep autoscroll
        try:
            out.write(text)
        except Exception:
            # Fallback to update
            self._output_lines.append(text)
            out.update("\n".join(self._output_lines))

    def _show_output_panel(self) -> None:
        """Hide the form and show the output log nearly fullscreen."""
        # Hide title and form
        try:
            self.query_one("#form_container").display = False  # type: ignore[attr-defined]
        except Exception:
            try:
                self.query_one("#form_container").styles.display = "none"  # type: ignore[attr-defined]
            except Exception:
                pass
        try:
            self.query_one("#title", Label).display = False  # type: ignore[attr-defined]
        except Exception:
            try:
                self.query_one("#title", Label).styles.display = "none"  # type: ignore[attr-defined]
            except Exception:
                pass
        # Show output title and log
        for sel in ("#output_title", "#output_log"):
            try:
                self.query_one(sel).display = True  # type: ignore[attr-defined]
            except Exception:
                try:
                    self.query_one(sel).styles.display = "block"  # type: ignore[attr-defined]
                except Exception:
                    pass

    # Progress bar removed

    def _run_setups_worker(self, data: Dict[str, Any]) -> None:
        current_dir = os.getcwd()
        chosen_name = (data.get("project_name") or os.path.basename(current_dir)).strip()
        if os.path.basename(current_dir) == chosen_name:
            project_root = current_dir
        else:
            project_root = os.path.join(current_dir, chosen_name)
            os.makedirs(project_root, exist_ok=True)
        self.project_dir = project_root
        project_name = os.path.basename(self.project_dir)

        steps: list[tuple[str, str]] = []
        if data.get("backend_framework") == "django":
            steps.append(("django", "Setting up Django"))
        if data.get("frontend_framework") == "vue":
            steps.append(("vue", "Setting up Vue + Vite"))
        if data.get("include_docker"):
            steps.append(("docker", "Creating Docker files"))

        total = len(steps)

        def do_log(text: str) -> None:
            self.app.call_from_thread(self.log_line, text)

        if total == 0:
            do_log("No setup steps selected.")
            def _enable_submit() -> None:
                try:
                    self.query_one("#submit", Button).disabled = False
                except Exception:
                    pass
            self.app.call_from_thread(_enable_submit)
            return

        do_log(f"Project: {project_name} — at {self.project_dir}")
        completed = 0
        for key, title in steps:
            try:
                if key == "django":
                    if data.get("include_unfold") and data.get("backend_framework") != "django":
                        do_log("Warning: 'Unfold' option requires Django backend; ignoring.")
                    setup_django(self, is_unfold=bool(data.get("include_unfold")))
                    do_log("Django setup completed.")
                elif key == "vue":
                    setup_vue(self)
                    do_log("Vue setup completed.")
                elif key == "docker":
                    setup_docker(self)
                    do_log("Docker files created.")
            except Exception as e:
                do_log(f"{title} failed: {e}")
            finally:
                completed += 1
                # No progress bar

        do_log("All requested setup steps finished.")
        def _enable_submit() -> None:
            try:
                self.query_one("#submit", Button).disabled = False
            except Exception:
                pass
        self.app.call_from_thread(_enable_submit)

    def on_project_setup_form_submitted(self, message: ProjectSetupForm.Submitted) -> None:
        try:
            self.query_one("#submit", Button).disabled = True
        except Exception:
            pass
        # Switch UI to output-focused view
        self._show_output_panel()
        threading.Thread(target=self._run_setups_worker, args=(message.data,), daemon=True).start()
