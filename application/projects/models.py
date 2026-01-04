from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from application.extensions import db


class Base(DeclarativeBase):
    pass


class Projects(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    project_name:Mapped[str] = mapped_column(String(120), nullable= False)
    image:Mapped[str] = mapped_column(String(120), nullable= False)
    url:Mapped[str] = mapped_column(String(120), nullable= False)
    description:Mapped[str] = mapped_column(String(120), nullable= False)