import os

# Automatically bind to the PORT environment variable provided by Render (default 10000) or local (5050)
port = os.environ.get("PORT", "5050")
bind = f"0.0.0.0:{port}"

workers = 2
threads = 4
timeout = 120
keepalive = 5
