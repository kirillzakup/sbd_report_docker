import os, sys, importlib.util
from pathlib import Path
import threading

# Find the first app.py within 4 levels
repo_root = Path(__file__).resolve().parent
candidates = list(repo_root.rglob("app.py"))
if not candidates:
    print("❌ app.py not found in repository")
    sys.exit(1)

app_py = candidates[0]
app_dir = app_py.parent
sys.path.insert(0, str(app_dir))

# Load app.py as module named "app"
spec = importlib.util.spec_from_file_location("app", str(app_py))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Try to start Telegram bot polling if available
bot = getattr(mod, "bot", None)
token = getattr(mod, "TOKEN", None) or os.environ.get("TELEGRAM_BOT_TOKEN")
if bot and token:
    t = threading.Thread(target=getattr(bot, "infinity_polling"), kwargs={"timeout": 10, "logger_level": None}, daemon=True)
    t.start()
    print("✅ Telegram bot polling started")

# Run Flask app
flask_app = getattr(mod, "app", None)
if flask_app is None:
    print("❌ Flask app object 'app' not found in app.py")
    sys.exit(1)

port = int(os.environ.get("PORT", "5000"))
print(f"✅ Starting Flask on 0.0.0.0:{port} (via run.py)")
flask_app.run(host="0.0.0.0", port=port, debug=False)
