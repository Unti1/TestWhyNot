import asyncio
import os
from time import monotonic
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем параметры из переменной окружения
SLEEP_DURATION = float(os.getenv("SLEEP_DURATION", 3))

app = FastAPI()
router = APIRouter()

# Модель ответа
class TestResponse(BaseModel):
    elapsed: float

# Блокировка для предотвращения параллельного выполнения work
lock = asyncio.Lock()

# Функция work, которая спит указанное время
async def work() -> None:
    await asyncio.sleep(SLEEP_DURATION)

# Обработчик маршрута
@router.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    async with lock:  # Предотвращаем одновременное выполнение
        ts1 = monotonic()  # Начало отсчета
        await work()
        ts2 = monotonic()  # Окончание отсчета
    return TestResponse(elapsed=ts2 - ts1)

# Добавляем роутер в приложение
app.include_router(router)
