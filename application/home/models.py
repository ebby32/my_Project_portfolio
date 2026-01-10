from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


from application.extensions import db


class Base(DeclarativeBase):
    pass

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('username', name= 'uq_users_username'),
    )
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String(100), nullable = False)
    password:Mapped[str] = mapped_column(String(100), nullable= False)

    projects:Mapped[List["Projects"]] = relationship(back_populates="users")
    notes:Mapped[List['Notes']] = relationship(back_populates='users')



class Projects(db.Model):
    __tablename__ = "projects"
    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    project_name:Mapped[str] = mapped_column(String(120), nullable= False)
    image:Mapped[str] = mapped_column(String(120), nullable= False)
    url:Mapped[str] = mapped_column(String(120), nullable= False)
    description:Mapped[str] = mapped_column(String(120), nullable= False)

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", name= 'fk_projects_user_id'), nullable=True)
    users:Mapped['Users'] = relationship(back_populates='projects')
