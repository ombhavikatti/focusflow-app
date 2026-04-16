from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

def categorize(task):
    task = task.lower()
    if "study" in task or "exam" in task:
        return "Study"
    elif "project" in task or "work" in task:
        return "Work"
    else:
        return "Personal"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('task')
        priority = request.form.get('priority')

        if text:
            tasks.append({
                "text": text,
                "priority": priority,
                "category": categorize(text),
                "done": False
            })
            save_data()

        return redirect('/')

    completed = sum(1 for t in tasks if t['done'])
    total = len(tasks)

    return render_template("index.html",
                           tasks=tasks,
                           completed=completed,
                           total=total)

@app.route('/complete/<int:index>')
def complete(index):
    tasks[index]['done'] = True
    save_data()
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks.pop(index)
    save_data()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)