from fastapi import APIRouter, HTTPException
from todo.repository import TaskRepository
from todo.schemas import TaskCreate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("/create", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """
    Создание новой задачи

    - Принимает объект TaskCreate
    - Возвращает созданную задачу с ID
    - В случае ошибки возвращает 400 статус
    """
    try:
        return await TaskRepository.add_task(task)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка создания задачи: {str(e)}"
        )


@router.get("/get-all", response_model=list[TaskResponse])
async def get_tasks():
    """
    Получение списка всех задач

    - Возвращает массив задач с ID
    - В случае ошибки возвращает 500 статус
    """
    try:
        return await TaskRepository.find_all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения задач: {str(e)}"
        )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskCreate):
    """
    Обновление задачи

    - Принимает ID задачи и новые данные
    - Возвращает обновленную задачу
    - 404 если задача не найдена
    - 500 для других ошибок
    """
    try:
        return await TaskRepository.update_task(task_id, task_update)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Задача не найдена: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обновления задачи: {str(e)}"
        )


@router.delete("/{task_id}", response_model=bool)
async def delete_task(task_id: int):
    """
    Удаление задачи по ID

    - Принимает ID задачи
    - Возвращает успешность удаления
    - 404 если задача не найдена
    - 500 для других ошибок
    """
    try:
        return await TaskRepository.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Задача не найдена: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка удаления задачи: {str(e)}"
        )