from todo.database import new_session, TaskORM
from sqlalchemy import select
from todo.schemas import TaskCreate, TaskResponse


class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskCreate) -> TaskResponse:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            await session.refresh(task)
            return task

    @classmethod
    async def find_all(cls) -> list[TaskCreate]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [task_model.__dict__ for task_model in task_models]
            return task_schemas

    @classmethod
    async def update_task(cls, task_id: int, task_update: TaskCreate) -> TaskResponse:
        async with new_session() as session:
            query = select(TaskORM).filter_by(id=task_id)
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()

            if not task_model:
                raise ValueError("Задача не найдена")

            # Обновляем поля задачи
            for key, value in task_update.model_dump(exclude_unset=True).items():
                setattr(task_model, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(task_model)
            return task_model

    @classmethod
    async def delete_task(cls, task_id: int) -> bool:
        async with new_session() as session:
            task_model = await session.get(TaskORM, task_id)

            if not task_model:
                raise ValueError("Задача не найдена")

            await session.delete(task_model)
            await session.commit()
            return True