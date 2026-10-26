from datetime import date
from fastapi import APIRouter, HTTPException, status
from models import (
    BirthdayRequest,
    InvalidItemIDException,
    UserCreate,
    UserResponse,
)

router = APIRouter()

# Banco de dados simulado em memória para os Exercícios 9 e 10
fake_items_db = {
    1: {"item_id": 1, "name": "Laptop", "price": 3500.0},
    2: {"item_id": 2, "name": "Mouse", "price": 150.0},
    3: {"item_id": 3, "name": "Teclado", "price": 300.0},
}


# Exercício 2: Rota principal
@router.get("/", summary="Rota principal")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Exercício 3: Rota /status
@router.get("/status", summary="Status do Servidor")
def get_status():
    return {"status": "ok", "message": "O servidor está funcionando perfeitamente."}


# Exercício 3, 5 e 6: Rota /user/{username} com Response Model e tratamento 404
@router.get(
    "/user/{username}",
    response_model=UserResponse,
    summary="Saudação personalizada ao usuário",
)
def get_user(username: str):
    # Lista simulada de usuários existentes para validação do 404
    valid_users = ["john", "alice", "bob", "maria"]

    if username.lower() not in valid_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário '{username}' não encontrado.",
        )

    return {"username": username, "message": f"Welcome, {username}!"}


# Exercício 7 e 8: Rota POST /create-user com validação Pydantic
@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
)
def create_user(user: UserCreate):
    return {
        "message": "Usuário criado com sucesso!",
        "data": {"username": user.username, "age": user.age},
    }


# Exercício 9 e 10: Rota /item/{item_id} suportando GET e DELETE com exceção personalizada
@router.get("/item/{item_id}", summary="Obter item por ID")
def get_item(item_id: int):
    # Exercício 10: Validação personalizada se item_id for menor ou igual a 0
    if item_id <= 0:
        raise InvalidItemIDException(item_id)

    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado."
        )

    return {"item": fake_items_db[item_id]}


@router.delete("/item/{item_id}", summary="Remover item por ID")
def delete_item(item_id: int):
    if item_id <= 0:
        raise InvalidItemIDException(item_id)

    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado."
        )

    removed_item = fake_items_db.pop(item_id)
    return {
        "message": f"Item {item_id} removido com sucesso.",
        "item": removed_item,
    }


# Exercício 11: Rota POST /birthday para cálculo de dias até o próximo aniversário
@router.post("/birthday", summary="Calcular dias até o próximo aniversário")
def calculate_birthday(data: BirthdayRequest):
    today = date.today()
    birth_date = date.fromisoformat(data.birthday)

    # Definir o próximo aniversário no ano atual ou próximo
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)

    days_remaining = (next_birthday - today).days

    return {
        "name": data.name,
        "days_remaining": days_remaining,
        "message": f"Olá, {data.name}! Faltam {days_remaining} dias para o seu próximo aniversário.",
    }