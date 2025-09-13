from textual.app import ComposeResult, App
from textual.widgets import Button, Label, Static, Link
from textual.containers import Vertical
from textual_pyfiglet import FigletWidget
import requests
import time
import threading
import os

# Never hard-code secrets; use env vars if needed
CLIENT_ID = os.environ.get("CLIENT_ID", "Ov23livfQfAoGENnwFcK")


class AuthFlow(App):
    CSS = """
    #status { height: auto; }
    #verify_link { padding-top: 1; }
    #code_box { height: 8; }
    """

    def compose(self) -> ComposeResult:
        yield Label("Authenticate with GitHub to continue.")
        with Vertical():
            yield Button("Start Authentication", id="start_auth", variant="primary")
            yield Static("", id="status")
            yield Link("Open verification page", url="https://github.com/login/device", id="verify_link")
            yield Static("", id="code_box")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_auth":
            self.query_one("#start_auth", Button).disabled = True
            threading.Thread(target=self._run_device_flow, daemon=True).start()

    # UI helpers
    def _set_status(self, text: str) -> None:
        self.query_one("#status", Static).update(text)

    def _show_code(self, verification_uri: str, user_code: str) -> None:
        # Update status and show a clickable link
        self._set_status("Open the link and enter this code:")
        try:
            link = self.query_one("#verify_link", Link)
            try:
                link.url = verification_uri  # type: ignore[attr-defined]
            except Exception:
                pass
            try:
                link.update(verification_uri)
            except Exception:
                pass
        except Exception:
            pass
        box = self.query_one("#code_box", Static)
        # Clear previous content if any
        try:
            for child in list(box.children):
                child.remove()
        except Exception:
            pass
        # Create figlet and set font without chaining (set_font returns None)
        try:
            fig = FigletWidget(user_code, font="smbraille", justify="center", id="figlet")
        except TypeError:
            fig = FigletWidget(user_code)
            try:
                fig.set_font("big")
            except Exception:
                pass

        box.mount(fig)
        # Optionally copy code to clipboard, if supported
        try:
            fw = self.query_one("#figlet", FigletWidget)
            if hasattr(fw, "copy_text_to_clipboard"):
                fw.copy_text_to_clipboard()
        except Exception:
            pass

    # Worker
    def _run_device_flow(self) -> None:
        try:
            resp = requests.post(
                "https://github.com/login/device/code",
                data={"client_id": CLIENT_ID, "scope": "read:user"},
                headers={"Accept": "application/json"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            device_code = data["device_code"]
            user_code = data["user_code"]
            verification_uri = data["verification_uri"]
            interval = int(data.get("interval", 5))

            self.call_from_thread(self._show_code, verification_uri, user_code)

            access_token = None
            while True:
                auth_resp = requests.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": CLIENT_ID,
                        "device_code": device_code,
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    },
                    headers={"Accept": "application/json"},
                    timeout=10,
                )
                auth_resp.raise_for_status()
                token_data = auth_resp.json()

                if "access_token" in token_data:
                    access_token = token_data["access_token"]
                    break
                err = token_data.get("error")
                if err == "authorization_pending":
                    time.sleep(interval)
                    continue
                if err == "slow_down":
                    interval += 5
                    time.sleep(interval)
                    continue
                raise RuntimeError(f"Device flow error: {token_data}")

            user_resp = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            user_resp.raise_for_status()
            user = user_resp.json()
            self.call_from_thread(
                self._set_status,
                f"Logged in as {user.get('login')} (ID: {user.get('id')})",
            )
        except Exception as e:
            self.call_from_thread(self._set_status, f"Auth failed: {e}")
        finally:
            try:
                self.call_from_thread(
                    setattr, self.query_one("#start_auth", Button), "disabled", False
                )
            except Exception:
                pass


if __name__ == "__main__":
    AuthFlow().run()
