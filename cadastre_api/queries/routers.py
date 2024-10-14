import asyncio
import random

from config import db_helper
from fastapi import APIRouter, Depends, HTTPException, status
from queries.models import Query
from queries.schemas import QueryCreate, QueryResponse, ResultResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.services import oauth2_scheme

router = APIRouter(tags=["Queries"])


@router.get("/ping")
async def ping():
    """
    Проверяет, что сервер запустился.
    """
    await asyncio.sleep(1)
    return {"message": "Server is up!"}


@router.post("/query", response_model=QueryResponse)
async def send_query(
    request: QueryCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Сохраняет в базу данных параметры запроса
    и возвращает идентификатор запроса.
    """
    new_query = Query(
        cadastre_number=request.cadastre_number,
        latitude=request.latitude,
        longitude=request.longitude,
        result=None,
    )
    db.add(new_query)
    await db.commit()
    await db.refresh(new_query)

    return QueryResponse(id=new_query.id)


@router.get("/result", response_model=ResultResponse)
async def get_result(
    query_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Эмулирует запрос на сервер по идентификатору
    и возвращает результат в виде булевого значения.
    """
    query = await db.get(Query, query_id)

    if not query:
        # Если запрос не найден, выдаем код 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Query not found"
        )

    # Эмуляция запроса на внешний сервер
    await asyncio.sleep(random.randint(1, 60))  # До 60 секунд ожидания

    if query.result is None:
        # Если результат еще не определен, эмулируем его получение
        query.result = random.choice([True, False])
        await db.commit()
        await db.refresh(query)

    return ResultResponse(result=query.result)


@router.get("/history")
async def get_history(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db_helper.session_getter),
    number: str | None = None,
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
                detail="History not found for the given cadastre number",
            )

    return history
