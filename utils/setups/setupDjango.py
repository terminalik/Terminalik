import sys
import os
import subprocess
import shutil

def setup_django(self=None, is_unfold=False):
    logger = getattr(self, "log_line", print)
    logger("Setting up Django Project...")

    # Check if python is available
    if not shutil.which("python") and not shutil.which("python3"):
        print("Python is required to set up a Django project. Please install it and ensure it is available in PATH.")
        return

    # Determine project directory (supports being called with or without `self`)
    project_dir = getattr(self, "project_dir", os.getcwd())

    # Create project directory
    backend_dir = os.path.join(project_dir, "backend")
    os.makedirs(backend_dir, exist_ok=True)

    # Create virtual environment
    _run_and_log(logger, [sys.executable, "-m", "venv", "venv"], cwd=backend_dir)

    # Determine pip executable
    if os.name == "nt":
        pip_executable = os.path.join(backend_dir, "venv", "Scripts", "pip.exe")
    else:
        pip_executable = os.path.join(backend_dir, "venv", "bin", "pip")

    # Install dependencies (PyPI package for Unfold is "django-unfold")
    dependencies = ["Django", "djangorestframework", "django-cors-headers"]
    if is_unfold:
        dependencies.append("django-unfold")
    _run_and_log(logger, [pip_executable, "install"] + dependencies, cwd=backend_dir)

    # Create Django project
    if os.name == "nt":
        django_admin = os.path.join(backend_dir, "venv", "Scripts", "django-admin.exe")
    else:
        django_admin = os.path.join(backend_dir, "venv", "bin", "django-admin")

    _run_and_log(logger, [django_admin, "startproject", "core", "."], cwd=backend_dir)

    # Create requirements.txt
    with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
        f.write("\n".join(dependencies))

    # Update settings.py
    settings_path = os.path.join(backend_dir, "core", "settings.py")
    with open(settings_path, "r") as f:
        content = f.read()

    if is_unfold:
        unfold_setting = """
UNFOLD = {
    "SITE_TITLE": "Terminalik Admin",
    "SITE_HEADER": "Terminalik Admin",
    "SITE_URL": "/",
    "SITE_SYMBOL": "settings"
}
"""
    content = content.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n    'corsheaders',\n    'rest_framework',\n    'unfold',\n    'unfold.contrib.forms',"
    )
    if is_unfold:
        content = content.replace(
            "from pathlib import Path",
            "from pathlib import Path\n\n" + unfold_setting
        )
    content = content.replace(
        "MIDDLEWARE = [",
        "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
    )

    # Add CORS settings at the end
    cors_settings = """
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
"""
    content += cors_settings

    # Ensure ALLOWED_HOSTS allows dev via Docker
    content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = [\"*\", \"localhost\", \"127.0.0.1\"]")

    with open(settings_path, "w") as f:
        f.write(content)

    # Create an app
    _run_and_log(logger, [django_admin, "startapp", "terminalik"], cwd=backend_dir)

    # Add import to admin.py
    if is_unfold:
        unfold_admin_import = """from unfold.admin import ModelAdmin

#@admin.register(MyModel)
#class CustomAdminClass(ModelAdmin):
#    pass"""

    if is_unfold:
        admin_path = os.path.join(backend_dir, "terminalik", "admin.py")
        with open(admin_path, "a") as f:
            f.write("\n" + unfold_admin_import + "\n")

    # Install requirements
    _run_and_log(logger, [pip_executable, "install", "-r", "requirements.txt"], cwd=backend_dir)

    # Migrate database
    py_exec = os.path.join(backend_dir, "venv", "bin", "python") if os.name != "nt" else os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    _run_and_log(logger, [py_exec, "manage.py", "migrate"], cwd=backend_dir)

    logger("Django Project setup complete.")


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
