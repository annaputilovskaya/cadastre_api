from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    username: str = Field(title="username")
    email: EmailStr | None = Field(title="email", default=None)
    password: str = Field(title="password", min_length=8)


class Token(BaseModel):
    """
    Model for describing JWT tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class RefreshToken(BaseModel):
    """
    Model for describing JWT tokens for refresh tokens.
    """
    refresh_token: str
