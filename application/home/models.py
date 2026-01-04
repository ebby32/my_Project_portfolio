from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from application.extensions import db


class Base(DeclarativeBase):
    pass

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String(100), nullable = False, unique= True)
    password:Mapped[str] = mapped_column(String(100), nullable= False)



class Projects(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    project_name:Mapped[str] = mapped_column(String(120), nullable= False)
    image:Mapped[str] = mapped_column(String(120), nullable= False)
    url:Mapped[str] = mapped_column(String(120), nullable= False)
    description:Mapped[str] = mapped_column(String(120), nullable= False)
