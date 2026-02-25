import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "habitTracker")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing. Add it to your .env file.")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
tasks = db["tasks"]


@app.route("/")
def index():
    # Show newest first
    all_tasks = list(tasks.find().sort("created_at", -1))
    return render_template("index.html", todos=all_tasks)


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        tasks.insert_one({
            "title": title,
            "done": False,
            "created_at": datetime.utcnow()
        })
    return redirect(url_for("index"))


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle(task_id):
    """
    Toggle done = True/False in MongoDB.
    """
    task = tasks.find_one({"_id": ObjectId(task_id)}, {"done": 1})
    if not task:
        return redirect(url_for("index"))

    new_done = not bool(task.get("done", False))
    tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"done": new_done}}
    )
    return redirect(url_for("index"))


@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    """
    Permanently delete the task from MongoDB.
    """
    tasks.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)