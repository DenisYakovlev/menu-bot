import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base


# class MealMenuRelation(Base):
#     __tablename__ = "menu_meal_relation"

#     menu_id = sa.Column(sa.Integer, sa.ForeignKey("menu.id"), primary_key=True)
#     meal_id = sa.Column(sa.Integer, sa.ForeignKey("meal.id"), primary_key=True)

#     menus = relationship("Menu", back_populates="meals")
#     meals = relationship("Meal", back_populates="menus")


meal_menu_relation = sa.Table(
    "meal_menu_relation",
    Base.metadata,
    sa.Column("menu_id", sa.ForeignKey("menu.id"), primary_key=True),
    sa.Column("meal_id", sa.ForeignKey("meal.id"), primary_key=True),
    extend_existing=True,
)