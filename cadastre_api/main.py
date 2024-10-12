import uvicorn
from fastapi import FastAPI

from config.config import settings

from queries import router as queries_router
from users import router as users_router

app = FastAPI(
    title="Cadastre API"
)

app.include_router(queries_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)