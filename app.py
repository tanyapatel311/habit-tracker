import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

app = Flask(__name__)

# ________MongoDB setup________
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "habitTracker")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing. Add it to your .env file.")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
tasks = db["tasks"]  # collection (like a table)

@app.route("/")
def index():
    """READ: fetch tasks from MongoDB and show them on the homepage."""
    all_tasks = list(tasks.find().sort("created_at", -1))
    return render_template("index.html", todos=all_tasks)

@app.route("/new")
def new():
    """ Shows the form page. """
    return render_template("new.html")

@app.route("/add", methods=["POST"])
def add():
    """ CREATE: insert a new task into MongoDB."""
    title = request.form.get("title", "").strip()

    if title:
        tasks.insert_one({
            "title": title,
            "done": False,
            "created_at": datetime.utcnow()
        })

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)