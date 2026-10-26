from datetime import date
from pydantic import BaseModel, Field, field_validator


# Exercício 5 e 6: Modelo de resposta para usuário
class UserResponse(BaseModel):
    username: str
    message: str


# Exercício 8: Modelo Pydantic para criação de usuário com validação
class UserCreate(BaseModel):
    username: str = Field(..., description="Nome de usuário deve ser uma string")
    age: int = Field(..., gt=0, description="A idade deve ser um número inteiro positivo")


# Exercício 11: Modelo para dados de aniversário
class BirthdayRequest(BaseModel):
    name: str = Field(..., description="Nome da pessoa")
    birthday: str = Field(..., description="Data de aniversário no formato YYYY-MM-DD")

    @field_validator("birthday")
    def validate_birthday_format(cls, value: str) -> str:
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("A data deve estar no formato válido YYYY-MM-DD")
        return value


# Exercício 10: Exceção personalizada para item_id inválido
class InvalidItemIDException(Exception):

    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = (
            f"O ID do item '{item_id}' é inválido. Deve ser um número inteiro positivo."
        )