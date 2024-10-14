import asyncio
import random

from fastapi import APIRouter
from sqlalchemy import select

from config import db_helper
from queries.models import Query
from queries.schemas import QueryCreate
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=['Queries']
)


@router.get("/ping")
async def ping():
    """
    Проверяет, что сервер запустился.
    """
    await asyncio.sleep(1)
    return {"message": "Server is up!"}


@router.post("/query")
async def send_query(
        request: QueryCreate,
        db: AsyncSession = Depends(db_helper.session_getter)
        ):
    """
    Сохраняет в базу данных параметры запроса
    и возвращает идентификатор запроса.
    """
    new_query = Query(
    cadastre_number = request.cadastre_number,
    latitude = request.latitude,
    longitude = request.longitude,
    result = None
)
    db.add(new_query)
    await db.commit()
    await db.refresh(new_query)

    return {"query_id": new_query.id}


@router.get("/result")
async def get_result(
        query_id: int,
        db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Эмулирует запрос на сервер по идентификатору
    и возвращает результат в виде булевого значения.
    """
    try:
        query = await db.get(Query, query_id)
        if not query:
            return {"message": "Query not found"}
        else:
            # Эмуляция запроса на внешний сервер
            await asyncio.sleep(random.randint(1, 60))  # До 60 секунд ожидания

            if  query.result is not None:
                pass

            else:
                result = random.choice([True, False])
                query.result = result
                await db.commit()
                await db.refresh(query)

            return {"result": query.result}

    except Exception:
            # Передать ошибку разработчикам
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong")


@router.get("/history")
async def get_history(
        db: AsyncSession = Depends(db_helper.session_getter),
        number: str | None = None
):
    """
   Получает историю запросов по кадастровому номеру
   или историю всех запросов, если кадастровый номер не указан.
    """
    if number is None:
        # История всех запросов
        result = await db.execute(select(Query))
        history = result.scalars().all()
    else:
        # История запросов по кадастровому номеру
        result = await db.execute(select(Query).where(Query.cadastre_number == number))
        history = result.scalars().all()

        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="History not found for the given cadastre number")

    return history
