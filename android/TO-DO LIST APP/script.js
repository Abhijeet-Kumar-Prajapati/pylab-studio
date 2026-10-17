document.addEventListener('DOMContentLoaded', loadTasks);
document.getElementById('addTaskBtn').addEventListener('click', addTask);

function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.forEach(task => displayTask(task));
}

function addTask() {
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const dueDate = document.getElementById('taskDueDate').value;
    const priority = document.getElementById('taskPriority').value;

    if (title) {
        const task = {
            id: Date.now(),
            title,
            description,
            dueDate,
            priority,
            completed: false
        };
        saveTask(task);
        displayTask(task);
        clearInputs();
    }
}

function saveTask(task) {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function displayTask(task) {
    const taskList = document.getElementById('taskList');
    const taskItem = document.createElement('li');
    taskItem.className = `task-item ${task.completed ? 'completed' : ''}`;
    taskItem.innerHTML = `
        <div>
            <strong>${task.title}</strong> <br>
            <span>${task.description}</span> <br>
            <span>Due: ${task.dueDate} | Priority: ${task.priority}</span>
        </div>
        <div>
            <button onclick="toggleCompletion(${task.id})">${task.completed ? 'Undo' : 'Complete'}</button>
            <button onclick="deleteTask(${task.id})">Delete</button>
        </div>
    `;
    taskList.appendChild(taskItem);
}

function toggleCompletion(id) {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    task.completed = !task.completed;
    localStorage.setItem('tasks', JSON.stringify(tasks));
    location.reload();
}

function deleteTask(id) {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    const remaining = tasks.filter(t => t.id !== id);
    localStorage.setItem('tasks', JSON.stringify(remaining));
    location.reload();
}

function clearInputs() {
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskDueDate').value = '';
    document.getElementById('taskPriority').value = 'low';
}