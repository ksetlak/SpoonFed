# SpoonFed
A complete nutrition delegation system

## Initial concept

SpoonFed as front end (to come later)
AutoMenu as back end (`automenu-api`)

### Back end plan

```mermaid
graph TD
    App[FastAPI App] --> Auth[Auth Router<br/>/auth/login]
    App --> Meals[Meals Router<br/>/api/meals]
    App --> Planner[Planner Router<br/>/api/layout]
```

+ planning endpoint? (`/api/v1/plans/generate`)
+ External API Integration? (Edamam or USDA Food Data Central)

ORM choice: SQLAlchemy. SQLModel was taken into account, but I want to have more work to do on purpose, to have more opportunity to practice. Specifically, to practice Pydantic in this case.

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
uv run init_env.py
```

... then get the DB password from the .env file and use with the next command:

```bash
podman machine start
podman run --name automenu-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v pgdata:/var/lib/postgresql -d docker.io/library/postgres
uv run seed.py
```

### Running tests

MacOS / Linux: `uv run pytest tests_backend -v`
On Windows: `automenu_api/.venv/Scripts/python.exe -m pytest tests_backend/ -v`

### Running the entire app

```bash
# Run the backend
podman start automenu-db
uv run fastapi dev
```

## Concepts to use

- Pydantic validation
- URL parameters
- Filtering
- Swagger
- Docker (layers, multi-stage builds)
- Tests
- Cloud

## Personas

Eater = a simple user that just cooks based on recipes retrieved from the app.

Chef = a curator that can add new recipes and modify existing ones.

## Inspirations

- [Paprika Recipe Manager](https://www.paprikaapp.com/)
- [Plan to Eat](https://www.plantoeat.com/)
- [Whisk / Samsung Food](https://samsungfood.com/)
- [Bring!](https://getbring.com/en/home)
- [Cebulko](https://cebulko.app/)
- [FeedMe](https://feed-me.app/)
