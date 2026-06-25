from typing import Annotated

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import connect_db
from models import Meal, User
from security import create_access_token, verify_password


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
session = AsyncSession(engine)


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


@app.post("/api/meals", response_model=MealReadModel)
async def create_meal(meal_in: MealCreateModel):
    async with AsyncSession(engine) as session:
        meal = Meal(**meal_in.model_dump())
        session.add(meal)
        await session.commit()
        await session.refresh(meal)  # This populates the meal.id
    return meal


@app.get("/api/meals/{meal_id}")
async def retrieve_meal(meal_id: int):
    async with AsyncSession(engine) as session:
        meal = await session.get(Meal, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal with this ID could not be found.")
        else:
            return MealReadModel.model_validate(meal)


@app.patch("/api/meals/{meal_id}", response_model=MealReadModel)
async def update_meal(updated_meal: MealReadModel):
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
