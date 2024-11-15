from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class TaskORM(Model):
    __tablename__ = "tasks"

    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)
