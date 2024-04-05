import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base


class MealType(Base):
    __tablename__ = "meal_type"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), unique=True, nullable=False)

    refered_meals = relationship("Meal", back_populates="meal_type", lazy="selectin")
