import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base
from .meal_menu_relation import meal_menu_relation


class Menu(Base):
    __tablename__ = "menu"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), nullable=False, unique=False)
    date = sa.Column(sa.Date, nullable=False)

    meals = relationship("Meal", secondary=meal_menu_relation, back_populates="menus", passive_deletes=True, lazy="selectin")
