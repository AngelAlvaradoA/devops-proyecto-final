import os
import platform
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HOSTNAME = platform.node()
ENVIRONMENT = os.getenv("ENVIRONMENT", "desarrollo")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>DevOps Proyecto Final - Sistemas Operativos II</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f2f5; }
        .card { background: white; border-radius: 12px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #1a73e8; }
        .info { margin: 20px 0; font-size: 18px; }
        .label { font-weight: bold; color: #555; }
        .value { color: #333; }
        .badge { background: #1a73e8; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>DevOps Proyecto Final - Sistemas Operativos II</h1>
        <div class="info">
            <p><span class="label">Hostname:</span> <span class="value">{{ hostname }}</span></p>
            <p><span class="label">Ambiente:</span> <span class="badge">{{ environment }}</span></p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, hostname=HOSTNAME, environment=ENVIRONMENT)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "hostname": HOSTNAME})

@app.route("/info")
def info():
    return jsonify({
        "app": "DevOps Proyecto Final",
        "version": "1.0",
        "hostname": HOSTNAME,
        "environment": ENVIRONMENT
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
