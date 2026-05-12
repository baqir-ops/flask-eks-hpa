from flask import Flask, jsonify
import psutil
import platform
import time
import os

app = Flask(__name__)
START_TIME = time.time()


@app.route("/")
def index():
    return jsonify({
        "service": "flask-eks-dashboard",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("APP_ENV", "production"),
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    uptime = int(time.time() - START_TIME)
    return jsonify({
        "cpu_percent": cpu,
        "memory": {
            "total_mb": round(mem.total / 1024 / 1024, 2),
            "used_mb": round(mem.used / 1024 / 1024, 2),
            "percent": mem.percent,
        },
        "disk": {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
            "percent": disk.percent,
        },
        "uptime_seconds": uptime,
        "hostname": platform.node(),
        "platform": platform.system(),
    })


@app.route("/ready")
def ready():
    cpu = psutil.cpu_percent(interval=0.5)
    if cpu > 95:
        return jsonify({"status": "not ready", "reason": "CPU overloaded"}), 503
    return jsonify({"status": "ready"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
