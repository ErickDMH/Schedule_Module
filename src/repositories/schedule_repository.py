from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Optional
from src.core.models import ScheduledRoutineCreate, ScheduledRoutine

class ScheduleRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create(self, routine: ScheduledRoutineCreate) -> ScheduledRoutine:
        query = text("""
            INSERT INTO schedule_module.scheduled_routine 
            (name, category_id, start_date_time, end_date_time, description, note, recurrency)
            VALUES (:name, :category_id, :start_date_time, :end_date_time, :description, :note, :recurrency)
            RETURNING *
        """)
        result = await self.conn.execute(query, {
            "name": routine.name,
            "category_id": routine.category_id,
            "start_date_time": routine.start_date_time,
            "end_date_time": routine.end_date_time,
            "description": routine.description,
            "note": routine.note,
            "recurrency": routine.recurrency.value
        })
        row = result.fetchone()
        return ScheduledRoutine.model_validate(dict(row._mapping))

    async def get_by_id(self, routine_id: UUID) -> Optional[ScheduledRoutine]:
        query = text("SELECT * FROM schedule_module.scheduled_routine WHERE id = :id")
        result = await self.conn.execute(query, {"id": routine_id})
        row = result.fetchone()
        if row:
            return ScheduledRoutine.model_validate(dict(row._mapping))
        return None
