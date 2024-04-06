import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base
from .meal_menu_relation import meal_menu_relation
from .order import order_meal_relation


default_img_src = 'https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg'


class Meal(Base):
    __tablename__ = "meal"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256), unique=False, nullable=False)
    price = sa.Column(sa.Float, unique=False, nullable=False)
    img_url = sa.Column(sa.String(512), unique=False, nullable=True)
    type_id = sa.Column(sa.Integer, sa.ForeignKey("meal_type.id", ondelete="SET NULL"), nullable=True, default=default_img_src)

    meal_type = relationship("MealType", back_populates="refered_meals")
    menus = relationship("Menu", secondary=meal_menu_relation, back_populates="meals", passive_deletes=True, lazy="selectin")
    orders = relationship("Order", secondary=order_meal_relation, back_populates="meals")


