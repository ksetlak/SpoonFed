import os
import secrets

ENV_FILE = ".env"
ENV_TEMPLATE = ".env.example"

# Would be cool to use ENV_TEMPLATE as a dynamic template, but how to determine how to populate a field dynamically?
TEMPLATE_CONTENT = """DATABASE_URL=postgresql+asyncpg://user:PASSWORD_PLACEHOLDER@localhost:5432
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
