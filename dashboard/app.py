from flask import Flask, render_template_string
import redis
import os

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOpsHub Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #eef2f5;
            margin: 0;
            padding: 40px;
        }
        .container {
            background: white;
            max-width: 700px;
            margin: auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 10px #ccc;
        }
        h1 {
            color: #2c3e50;
        }
        .card {
            background-color: #f8f9fa;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }
        .number {
            font-size: 32px;
            font-weight: bold;
            color: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DevOpsHub Dashboard</h1>
        <p>This dashboard reads live data from Redis.</p>

        <div class="card">
            <h2>Total Messages Collected</h2>
            <p class="number">{{ message_count }}</p>
        </div>

        <div class="card">
            <h2>Total Visits to Message Page</h2>
            <p class="number">{{ visit_count }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    message_count = r.llen("messages")
    visit_count = r.get("visit_count")

    if visit_count is None:
        visit_count = 0

    return render_template_string(
        HTML_PAGE,
        message_count=message_count,
        visit_count=visit_count
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
