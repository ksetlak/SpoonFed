from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from jwt import PyJWTError, decode  # TODO: Potentially clean up
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import connect_db
from models import Meal, User
from security import create_access_token, validate_access_token, verify_password


class MealBase(BaseModel):
    name: str
    recipe: str
    calories: int
    carbs: float
    fat: float
    protein: float

    class Config:
        from_attributes = True


class MealCreateModel(MealBase):
    pass


class MealReadModel(MealBase):
    id: int


# TODO: Potentially move to security, unless we replace auth completely before that happens.
oauth2_scheme = HTTPBearer()


async def verify_admin_access(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        token_bytes = token.credentials.strip('"').encode("utf-8")
        decoded_token = decode(token_bytes, settings.jwt_secret_key, settings.jwt_algorithm)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from None
    if not validate_access_token(token_bytes, int(decoded_token["sub"])):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return int(decoded_token["sub"]) == 1


app = FastAPI()

origins = [
    "*"
    # "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = connect_db()


@app.post("/auth/login")
async def authenticate(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    async with AsyncSession(engine) as session:
        result = await session.scalars(select(User).where(User.username == username))
        user = result.one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    authenticated: bool = verify_password(user.hashed_password, user.password_salt, password)
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    jwt = create_access_token(user.id)
    return jwt


@app.post("/api/meals", response_model=MealReadModel, status_code=status.HTTP_201_CREATED)
async def create_meal(meal_in: MealCreateModel, admin_authorization: Annotated[bool, Depends(verify_admin_access)]):
    if not admin_authorization:
        raise HTTPException(status_code=403, detail="Insufficient permissions.")
    async with AsyncSession(engine) as session:
        meal = Meal(**meal_in.model_dump())
        session.add(meal)
        await session.commit()
        await session.refresh(meal)  # This populates the meal.id
    return meal


@app.get("/api/meals/{meal_id}", status_code=status.HTTP_200_OK)
async def retrieve_meal(meal_id: int):
    async with AsyncSession(engine) as session:
        meal = await session.get(Meal, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal with this ID could not be found.")
        else:
            return MealReadModel.model_validate(meal)


# TODO: meal_id is passed in URL, then id from body is uses. Analyze & fix.
@app.patch("/api/meals/{meal_id}", response_model=MealReadModel, status_code=status.HTTP_200_OK)
async def update_meal(updated_meal: MealReadModel, admin_authorization: Annotated[bool, Depends(verify_admin_access)]):
    if not admin_authorization:
        raise HTTPException(status_code=403, detail="Insufficient permissions.")
    async with AsyncSession(engine) as session:
        meal = await session.get(Meal, updated_meal.id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal with this ID could not be found.")
        else:
            update_data = updated_meal.model_dump(exclude_unset=True)  # Exclude unset just in case...
            for key, value in update_data.items():
                setattr(meal, key, value)
            await session.commit()
            await session.refresh(meal)
    return meal


@app.delete("/api/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(meal_id: int, admin_authorization: Annotated[bool, Depends(verify_admin_access)]):
    if not admin_authorization:
        raise HTTPException(status_code=403, detail="Insufficient permissions.")
    async with AsyncSession(engine) as session:
        meal = await session.get(Meal, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal with this ID could not be found.")
        else:
            session.delete(meal)
            await session.commit()
    return  # Or return None?
