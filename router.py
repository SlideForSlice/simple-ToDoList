from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from repository import TaskRepository
from schemas import TaskAdd, TasId

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/create")
async def add_task(
        task: Annotated[TaskAdd, Depends()],
) -> TasId:
    task_id = await TaskRepository.add_task(task)
    return {"ok": True, "task_id": task_id}

@router.get("/get-all")
async def get_task() -> list[TaskAdd]:

    tasks = await TaskRepository.find_all()
    return tasks
