from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Meal(Base):
    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    recipe: Mapped[str] = mapped_column(String(2000))
    calories: Mapped[int] = mapped_column(Integer)
    carbs: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f"Meal (id={self.id!r}, name={self.name!r})"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(60))
    password_salt: Mapped[str] = mapped_column(String(60))
