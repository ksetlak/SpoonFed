# SpoonFed
A complete nutrition delegation system

## Initial concept

SpoonFed as front end (to come later)
AutoMenu as back end (`automenu-api`)

### Back end plan

                      +-------------------+
                      |   FastAPI App     |
                      +---------+---------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
+-------v-------+       +-------v-------+       +-------v-------+
|  Auth Router  |       |  Meals Router |       | Planner Router|
| (/auth/login) |       |  (/api/meals) |       | (/api/layout) |
+---------------+       +---------------+       +---------------+

+ planning endpoint? (`/api/v1/plans/generate`)
+ External API Integration? (Edamam or USDA Food Data Central)

ORM choice: SQLModel (to acoid writing schema twice, once for Pydantic and once for SQLAlchemy)

Potential models:
- User: id, username, hashed_password, daily_calorie_target.
- Meal: id, name, calories, protein, carbs, fat, last_suggested_at.
- MealHistory: id, user_id, meal_id, date_consumed

## Quickstart

### Setup

After cloning the repo, make sure `uv` is installed.

```bash
uv sync
uv run pre-commit install
```

### Running the entire app

...

## Concepts to use

- Pydantic validation
- URL parameters
- Filtering
- Swagger
- Docker (layers, multi-stage builds)
- Tests
- Cloud

## Inspirations

- [Paprika Recipe Manager](https://www.paprikaapp.com/)
- [Plan to Eat](https://www.plantoeat.com/)
- [Whisk / Samsung Food](https://samsungfood.com/)
- [Bring!](https://getbring.com/en/home)
- [Cebulko](https://cebulko.app/)
- [FeedMe](https://feed-me.app/)
