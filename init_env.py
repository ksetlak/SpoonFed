import os
import secrets

ENV_FILE = ".env"
ENV_TEMPLATE = ".env.example"

# TODO: Would be cool to use ENV_TEMPLATE as a dynamic template, but how to determine how to populate a field dynamically?
# TODO: Break DATABASE_URL into POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT (?), POSTGRES_HOST (?)
TEMPLATE_CONTENT = """POSTGRES_PASSWORD=PASSWORD_PLACEHOLDER
DATABASE_URL=postgresql+asyncpg://spoonfed:PASSWORD_PLACEHOLDER@postgresql:5432/spoonfed
DEBUG=True
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=JWT_SECRET_PLACEHOLDER
JWT_VALIDITY=8760
"""


def generate_env():
    if os.path.exists(ENV_FILE):
        print(
            f"{ENV_FILE} file already exists! Skipping generation to avoid an unintended overwrite."
        )
        return

    print("Populating your local .env file...")

    db_password = secrets.token_urlsafe(16)
    jwt_secret = secrets.token_hex(32)

    env_content = TEMPLATE_CONTENT
    env_content = env_content.replace("PASSWORD_PLACEHOLDER", db_password)
    env_content = env_content.replace("JWT_SECRET_PLACEHOLDER", jwt_secret)

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"Successfully created and populated an {ENV_FILE} file.")


if __name__ == "__main__":
    generate_env()
