from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from todo.router import router as tasks_router
from todo.database import create_tables, engine, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("DB was deleted")
    await create_tables()
    print("DB was created")
    yield
    print("Turning off")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"]   # Разрешаем все заголовки
)
app.include_router(tasks_router)



