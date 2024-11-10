from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TaskResponse(TaskCreate):
    id: int


