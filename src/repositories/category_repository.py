from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Optional, List
from src.core.models import CategoryCreate, Category

class CategoryRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create(self, category: CategoryCreate) -> Category:
        query = text("""
            INSERT INTO schedule_module.category 
            (name, description, color, icon, image, note)
            VALUES (:name, :description, :color, :icon, :image, :note)
            RETURNING *
        """)
        result = await self.conn.execute(query, {
            "name": category.name,
            "description": category.description,
            "color": category.color,
            "icon": category.icon,
            "image": category.image,
            "note": category.note
        })
        row = result.fetchone()
        return Category.model_validate(dict(row._mapping))

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        query = text("SELECT * FROM schedule_module.category WHERE id = :id")
        result = await self.conn.execute(query, {"id": category_id})
        row = result.fetchone()
        if row:
            return Category.model_validate(dict(row._mapping))
        return None
