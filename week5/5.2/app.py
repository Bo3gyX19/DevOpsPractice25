from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the web application Version 2.0.0!"

@app.route('/version')
def version():
    return "Version: 2.0.0"

@app.route('/info')
def info():
    return jsonify({
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": os.environ.get("VERSION", "unknown"),
        "features": ["health-check", "version-info", "status-endpoint"]
    })

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    return jsonify({
        "status": "healthy",
        "version": "2.0.0",
        "uptime": "running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
