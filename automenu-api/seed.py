import asyncio
from getpass import getpass

from sqlalchemy.ext.asyncio import AsyncSession

from db import connect_db
from models import Base, Meal, User
from security import hash_password

seed_users = [
    {
        "username": "admin",
    }
]

seed_meals = [
    {
        "name": "Lentil & Tomato Stew",
        "recipe": "Sauté 1 diced onion, add 1 cup red lentils, 2 cups water, 1 cup przecier pomidorowy, and spices. Simmer 25 mins.",  # noqa
        "calories": 320,
        "carbs": 55.0,
        "fat": 2.5,
        "protein": 22.0,
    },
    {
        "name": "Tofu Stir-Fry",
        "recipe": "Stir-fry 200g tofu, 1 cup frozen peas, 1 cup frozen cauliflower, soy sauce, and garlic. Serve hot.",
        "calories": 280,
        "carbs": 20.0,
        "fat": 12.0,
        "protein": 24.0,
    },
    {
        "name": "Chickpea & Spinach Curry",
        "recipe": "Cook 1 can chickpeas, 2 cups spinach, 1 can diced tomatoes, coconut milk, and curry paste. Simmer 15 mins.",  # noqa
        "calories": 400,
        "carbs": 45.0,
        "fat": 14.0,
        "protein": 18.0,
    },
    {
        "name": "Red Bean Chili",
        "recipe": "Combine 1 can red beans, 1 can diced tomatoes, onion, chili powder, and cumin. Simmer 20 mins.",
        "calories": 350,
        "carbs": 50.0,
        "fat": 3.0,
        "protein": 20.0,
    },
    {
        "name": "Soy Chunks & Veggie Bowl",
        "recipe": "Rehydrate 100g soy chunks, mix with 1 cup frozen peas, carrots, and olive oil. Bake at 180°C for 15 mins.",  # noqa
        "calories": 300,
        "carbs": 25.0,
        "fat": 8.0,
        "protein": 25.0,
    },
]


async def prepare_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def seed_unattended(engine):
    async with AsyncSession(engine) as session:
        for meal in seed_meals:
            session.add(Meal(**meal))
        await session.commit()


async def seed_interactive(engine):
    async with AsyncSession(engine) as session:
        for user in seed_users:
            password = getpass(f"Provide a password for user: {user['username']} ...\n")
            user["hashed_password"] = hash_password(password)
            session.add(User(**user))
        await session.commit()


async def gathered(engine):
    await prepare_db(engine)
    await asyncio.gather(seed_unattended(engine), seed_interactive(engine))


if __name__ == "__main__":
    engine = connect_db()
    asyncio.run(gathered(engine))
