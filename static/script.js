const API_URL = 'http://127.0.0.1:8000';

// Создание задачи
async function createTask() {
    const nameInput = document.getElementById('taskName');
    const descriptionInput = document.getElementById('taskDescription');

    if (!nameInput.value) {
        alert('Введите название задачи');
        return;
    }

    const task = {
        name: nameInput.value,
        description: descriptionInput.value || null
    };

    try {
        const response = await fetch(`${API_URL}/tasks/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(task)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ошибка HTTP: ${response.status} - ${errorText}`);
        }

        const createdTask = await response.json();
        console.log('Созданная задача:', createdTask);

        // Очищаем поля ввода
        nameInput.value = '';
        descriptionInput.value = '';

        // Обновляем список задач
        await getAllTasks();

        alert('Задача успешно создана!');

    } catch (error) {
        console.error('Ошибка:', error);
        alert(`Не удалось создать задачу: ${error.message}`);
    }
}

// Получение всех задач
async function getAllTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks/get-all`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            // Получаем текст ошибки от сервера
            const errorText = await response.text();
            throw new Error(errorText || 'Ошибка при получении задач');
        }

        const tasks = await response.json();
        renderTasks(tasks);
        return tasks;
    } catch (error) {
        console.error('Ошибка получения задач:', error);
        alert(`Не удалось получить список задач: ${error.message}`);
        return [];
    }
}

// Редактирование задачи
async function startEditTask(id) {
    const taskElement = document.getElementById(`task-${id}`);
    if (!taskElement) return;

    const nameSpan = taskElement.querySelector('.task-name');
    const descSpan = taskElement.querySelector('.task-description');

    nameSpan.innerHTML = `<input type="text" id="edit-name-${id}" value="${nameSpan.textContent}" />`;
    descSpan.innerHTML = `<input type="text" id="edit-desc-${id}" value="${descSpan.textContent}" />`;

    const editButton = taskElement.querySelector('.edit-btn');
    editButton.innerHTML = 'Сохранить';
    editButton.onclick = () => saveEditTask(id);
}

// Сохранение отредактированной задачи
async function saveEditTask(id) {
    const nameInput = document.getElementById(`edit-name-${id}`);
    const descInput = document.getElementById(`edit-desc-${id}`);

    if (!nameInput.value) {
        alert('Название задачи не может быть пустым');
        return;
    }

    const updatedTask = {
        name: nameInput.value,
        description: descInput.value || null
    };

    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedTask)
        });

        if (!response.ok) {
            throw new Error('Ошибка при обновлении задачи');
        }

        await getAllTasks();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось обновить задачу');
    }
}

// Удаление задачи
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Ошибка при удалении задачи');
        }

        await getAllTasks();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить задачу');
    }
}

// Рендеринг списка задач
function renderTasks(tasks) {
    const taskList = document.getElementById('taskList');
    if (!taskList) return;

    // Очищаем текущий список
    taskList.innerHTML = '';

    // Создаем элементы для каждой задачи
    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.id = `task-${task.id}`;
        taskElement.className = 'task';
        taskElement.innerHTML = `
            <div>
                <span class="task-name">${task.name}</span>
                <span class="task-description">${task.description || ''}</span>
            </div>
            <div>
                <button class="edit-btn" onclick="startEditTask(${task.id})">Редактировать</button>
                <button onclick="deleteTask(${task.id})">Удалить</button>
            </div>
        `;

        taskList.appendChild(taskElement);
    });
}

// Инициализация списка задач при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    getAllTasks();
});