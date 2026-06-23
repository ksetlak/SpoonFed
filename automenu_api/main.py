from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from db import connect_db
from models import Meal

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


@app.get("/api/meals/{meal_id}")
async def get_meal(meal_id: int):
    async with AsyncSession(engine) as session:
        meal = await session.get(Meal, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal with this ID could not be found.")
        else:
            meal_dict = {
                "id": meal.id,
                "name": meal.name,
                "recipe": meal.recipe,
                "calories": meal.calories,
                "fat": meal.fat,
                "carbs": meal.carbs,
                "protein": meal.protein,
            }
            return meal_dict  # TODO: Update once pydantic is added: https://chat.mistral.ai/chat/5f4c9201-a25b-49ed-aff8-0a2f97db7850s
