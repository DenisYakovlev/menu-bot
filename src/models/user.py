import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.BigInteger, primary_key=True)
    phone_number = sa.Column(sa.String(20), unique=True, nullable=True)
    first_name = sa.Column(sa.String(256), unique=False, nullable=True)
    last_name = sa.Column(sa.String(256), unique=False, nullable=True)
    username = sa.Column(sa.String(256), unique=False, nullable=True)

    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    is_manager = sa.Column(sa.Boolean, nullable=False, default=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=func.now())

    orders = relationship("Order", back_populates="user")
    
