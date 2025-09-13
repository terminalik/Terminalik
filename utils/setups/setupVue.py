import os
import subprocess
import shutil
import re

def setup_vue(self=None):
    logger = getattr(self, "log_line", print)
    project_dir = getattr(self, "project_dir", os.getcwd())

    # Check if node and npm are available
    if not shutil.which("node") or not shutil.which("npm"):
        logger("Node.js and npm are required to set up a Vue project. Please install them and ensure they are available in PATH.")
        return

    # Create project directory
    frontend_dir = os.path.join(project_dir, "frontend")
    os.makedirs(frontend_dir, exist_ok=True)

    # Create Vue-ts project with Vite
    _run_and_log(logger, ["npm", "create", "vite@latest", "frontend", "--", "--template", "vue-ts"], cwd=project_dir)

    # Install dependencies
    _run_and_log(logger, ["npm", "install"], cwd=frontend_dir)

    # Change content to reflect Terminalik
    # Update <title> in index.html (handle variations of the default title)
    index_html_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_html_path):
        with open(index_html_path, "r", encoding="utf-8") as f:
            idx_content = f.read()
        # Replace any title content with "Terminalik"
        idx_content_new = re.sub(r"<title>.*?</title>", "<title>Terminalik</title>", idx_content, count=1, flags=re.IGNORECASE|re.DOTALL)
        if idx_content_new != idx_content:
            with open(index_html_path, "w", encoding="utf-8") as f:
                f.write(idx_content_new)

    # Update HelloWorld message in App.vue if present
    appvue_path = os.path.join(frontend_dir, "src", "App.vue")
    if os.path.exists(appvue_path):
        with open(appvue_path, "r", encoding="utf-8") as f:
            app_content = f.read()
        # Replace the msg attribute value on HelloWorld component if found
        app_content_new = re.sub(r"(<HelloWorld\s+msg=)\"[^\"]*\"", r'\1"Terminalik + Vite + Vue"', app_content, count=1)
        if app_content_new != app_content:
            with open(appvue_path, "w", encoding="utf-8") as f:
                f.write(app_content_new)

    # Ensure Node engine requirement for Vite 7+
    pkg_json_path = os.path.join(frontend_dir, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            import json
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            engines = pkg.get("engines", {})
            # Set a conservative engine range matching Vite's requirement
            engines["node"] = ">=20.19 <21 || >=22.12"
            pkg["engines"] = engines
            with open(pkg_json_path, "w", encoding="utf-8") as f:
                json.dump(pkg, f, indent=2)
        except Exception:
            pass

    # Write a simple .nvmrc to hint local Node version
    try:
        with open(os.path.join(frontend_dir, ".nvmrc"), "w", encoding="utf-8") as f:
            f.write("22\n")
    except Exception:
        pass


    logger("Vue project setup complete.")


def _run_and_log(logger, args, cwd=None):
    try:
        res = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if res.stdout:
            for line in res.stdout.splitlines():
                logger(line)
        if res.returncode != 0:
            logger(f"Command failed ({res.returncode}): {' '.join(args)}")
    except Exception as e:
        logger(f"Command error: {' '.join(args)} -> {e}")
