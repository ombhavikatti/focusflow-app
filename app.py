from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()

    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")

        if title:
            tasks.append({
                "title": title,
                "priority": priority,
                "status": "Pending",
                "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
            })
            save_tasks(tasks)

        return redirect("/")

    total = len(tasks)
    completed = len([t for t in tasks if t["status"] == "Done"])
    progress = int((completed / total) * 100) if total > 0 else 0

    return render_template("index.html",
                           tasks=tasks,
                           total=total,
                           completed=completed,
                           progress=progress)

@app.route("/complete/<int:index>")
def complete(index):
    tasks = load_tasks()
    tasks[index]["status"] = "Done"
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
