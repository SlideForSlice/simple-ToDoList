from database import new_session, TaskORM
from sqlalchemy import select
from schemas import TaskAdd


class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[TaskAdd]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalar().all()
            task_schemas = [TaskAdd.model_validate(task_model) for task_model in task_models]
            return task_schemas