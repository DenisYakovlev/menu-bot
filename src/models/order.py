from db import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


order_meal_relation = sa.Table('order_meal_relation', Base.metadata,
    sa.Column('order_id', sa.Integer, sa.ForeignKey('order.id')),
    sa.Column('meal_id', sa.Integer, sa.ForeignKey('meal.id'))
)


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    menu_id = sa.Column(sa.Integer, sa.ForeignKey("menu.id"), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False, unique=False)
    is_paid = sa.Column(sa.Boolean, nullable=False, default=False, server_default='0')

    user = relationship("User", back_populates="orders")
    menu = relationship("Menu", back_populates="orders")
    meals = relationship("Meal", secondary=order_meal_relation, back_populates="orders")
