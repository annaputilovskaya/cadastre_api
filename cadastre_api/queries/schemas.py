from pydantic import BaseModel, Field


class QueryCreate(BaseModel):
    """
    Схема создания запроса.
    """

    cadastre_number: str = Field(
        title="cadastre_number", pattern="^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,9}$"
    )
    latitude: str = Field(title="latitude", pattern="-?\d{1,3}\.\d+")
    longitude: str = Field(title="longitude", pattern="-?\d{1,3}\.\d+")


class QueryResponse(BaseModel):
    """
    Схема ответа на запрос.
    """

    id: int = Field(title="id")


class ResultResponse(BaseModel):
    """
    Схема результата запроса.
    """

    result: bool = Field(title="result")
