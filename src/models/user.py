import sqlalchemy as sa
from db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    phone_number = sa.Column(sa.String(20), unique=True, nullable=True)
    first_name = sa.Column(sa.String(256), unique=False, nullable=True)
    last_name = sa.Column(sa.String(256), unique=False, nullable=True)
    username = sa.Column(sa.String(256), unique=False, nullable=True)