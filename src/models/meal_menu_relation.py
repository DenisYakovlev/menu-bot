import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base


meal_menu_relation = sa.Table(
    "meal_menu_relation",
    Base.metadata,
    sa.Column("menu_id", sa.ForeignKey("menu.id"), primary_key=True),
    sa.Column("meal_id", sa.ForeignKey("meal.id"), primary_key=True),
    extend_existing=True,
)