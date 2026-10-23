import os

# Automatically bind to the PORT environment variable provided by Render/Heroku
port = os.environ.get("PORT", "5050")
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 2
threads = 4

# Generous timeout for OpenAI report generation
timeout = 120
keepalive = 5
