from pydantic import BaseModel, Field


class QueryCreate(BaseModel):
    """
    Модель создания запроса в API.
    """
    cadastre_number: str = Field(title='cadastre_number', pattern="^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,9}$")
    latitude: str = Field(title="latitude", pattern="-?\d{1,3}\.\d+")
    longitude: str = Field(title="longitude", pattern="-?\d{1,3}\.\d+")
