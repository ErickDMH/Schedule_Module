from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Optional, List
from datetime import datetime
from src.core.models import DateRegisterCreate, DateRegister

class DateRegisterRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create(self, register: DateRegisterCreate) -> DateRegister:
        query = text("""
            INSERT INTO schedule_module.date_register 
            (type, name, start_date_time, end_date_time, description, note, category_id, scheduled_routine_id, relationship_field)
            VALUES (:type, :name, :start_date_time, :end_date_time, :description, :note, :category_id, :scheduled_routine_id, :relationship_field)
            RETURNING *
        """)
        result = await self.conn.execute(query, {
            "type": register.type.value,
            "name": register.name,
            "start_date_time": register.start_date_time,
            "end_date_time": register.end_date_time,
            "description": register.description,
            "note": register.note,
            "category_id": register.category_id,
            "scheduled_routine_id": register.scheduled_routine_id,
            "relationship_field": register.relationship_field
        })
        row = result.fetchone()
        if row is None:
            raise RuntimeError("INSERT INTO date_register returned no row")
        return DateRegister.model_validate(dict(row._mapping))

    async def get_by_relationship(self, relationship_field: str) -> List[DateRegister]:
        query = text("SELECT * FROM schedule_module.date_register WHERE relationship_field = :rel")
        result = await self.conn.execute(query, {"rel": relationship_field})
        return [DateRegister.model_validate(dict(row._mapping)) for row in result.fetchall()]

    async def get_by_schedule(self, scheduled_routine_id: UUID) -> List[DateRegister]:
        query = text("SELECT * FROM schedule_module.date_register WHERE scheduled_routine_id = :sch")
        result = await self.conn.execute(query, {"sch": scheduled_routine_id})
        return [DateRegister.model_validate(dict(row._mapping)) for row in result.fetchall()]

    async def get_dates_from_range(self, start: datetime, end: datetime) -> List[DateRegister]:
        query = text("""
            SELECT * FROM schedule_module.date_register 
            WHERE start_date_time < :end AND end_date_time > :start
        """)
        result = await self.conn.execute(query, {"start": start, "end": end})
        return [DateRegister.model_validate(dict(row._mapping)) for row in result.fetchall()]
