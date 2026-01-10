from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.extensions import db



class Notes(db.Model):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(String(1000), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    body: Mapped[str] = mapped_column(String(1000), nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id', name='fk_notes_user_id'), nullable=True)
    users:Mapped['Users'] = relationship(back_populates='notes')
