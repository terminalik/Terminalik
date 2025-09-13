from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane, Static
from pages.projectSetup import ProjectSetupPane
from pages.readmeMarkdown import ReadmeMarkdown


class TerminalikApp(App):

    TITLE = "Terminalik"
    CSS_PATH = "terminalik.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(id="main_tabs"):
            with TabPane("General", id="general"):
                yield ReadmeMarkdown()
            with TabPane("Project Setup", id="project_setup"):
                yield ProjectSetupPane()
            with TabPane("Settings", id ="settings"):
                yield Static("Settings will be here.")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = TerminalikApp()
    app.run()
