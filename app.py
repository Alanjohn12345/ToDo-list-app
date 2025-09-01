from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
tasks = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_tasks")
def get_tasks():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for task in tasks:
        if task["done"]:
            task["status"] = "Completed"
        elif now < task["start"]:
            task["status"] = "Pending"
        elif task["start"] <= now <= task["end"]:
            task["status"] = "Ongoing"
        else:
            task["status"] = "Completed"
    return jsonify(tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()
    task = {
        "id": len(tasks)+1,
        "text": data["text"],
        "start": data["start"],
        "end": data["end"],
        "done": False,
        "status": "Pending"
    }
    tasks.append(task)
    return jsonify(task)

@app.route("/toggle_task/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/delete_task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
