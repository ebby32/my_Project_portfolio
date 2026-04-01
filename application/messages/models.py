
from sqlalchemy import Integer, nulls_last, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column

from application.extensions import db

class Messages(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key = True)
    sender_name:Mapped[str] = mapped_column(String(120), nullable = False )
    sender_email:Mapped[str] = mapped_column(String(120), nullable = False)
    telephone:Mapped[int] = mapped_column(Integer, nullable = False)
    message:Mapped[str] = mapped_column(String(1000), nullable = False)
    created_at:Mapped[str] = mapped_column(String(20), nullable= False)
    is_read:Mapped[bool] = mapped_column(Boolean, nullable = False, server_default= false() )
