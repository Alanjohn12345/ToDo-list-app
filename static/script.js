async function loadTasks() {
  const res = await fetch("/get_tasks");
  const tasks = await res.json();
  const list = document.getElementById("taskList");
  list.innerHTML = "";
  tasks.forEach(task => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${task.text}</span>
      <span class="status ${task.status}">${task.status}</span>
      <button onclick="deleteTask(${task.id})">❌</button>
    `;
    list.appendChild(li);
  });
}

async function addTask() {
  const input = document.getElementById("taskInput");
  const start = document.getElementById("startTime").value;
  const end = document.getElementById("endTime").value;
  if (!input.value || !start || !end) return alert("Please fill all fields!");
  await fetch("/add_task", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      text: input.value,
      start: start,
      end: end
    })
  });
  input.value = "";
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`/delete_task/${id}`, {method: "DELETE"});
  loadTasks();
}

window.onload = () => {
  loadTasks();
  setInterval(loadTasks, 30000); // auto-refresh every 30s
};
