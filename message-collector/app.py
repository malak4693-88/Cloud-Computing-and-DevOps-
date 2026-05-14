from flask import Flask, request, render_template_string, redirect
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
    <title>DevOpsHub Message Collector</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            margin: 0;
            padding: 40px;
        }
        .container {
            background: white;
            max-width: 600px;
            margin: auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 10px #ccc;
        }
        h1 {
            color: #2c3e50;
        }
        textarea {
            width: 100%;
            height: 120px;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .success {
            color: green;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DevOpsHub Message Collector</h1>
        <p>Submit your feedback, suggestion, or comment below.</p>

        <form method="POST" action="/submit">
            <textarea name="message" placeholder="Write your message here..." required></textarea>
            <br>
            <button type="submit">Submit Message</button>
        </form>

        {% if success %}
            <p class="success">Message submitted successfully!</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    r.incr("visit_count")
    success = request.args.get("success") == "true"
    return render_template_string(HTML_PAGE, success=success)

@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message")

    if message:
        r.rpush("messages", message)

    return redirect("/?success=true")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)