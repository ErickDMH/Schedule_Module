from uuid import UUID
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncConnection

from src.core.models import (
    ScheduledRoutineCreate, ScheduledRoutine, 
    DateRegisterCreate, DateRegister, RegisterType,
    CategoryCreate, Category
)
from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.date_register_repository import DateRegisterRepository
from src.repositories.category_repository import CategoryRepository
from src.db.connection import engine

class Schedule:
    """Primary service class for the Schedule Module"""

    def __init__(self, conn: Optional[AsyncConnection] = None):
        self._conn = conn

    async def __aenter__(self):
        if self._conn is None:
            self._engine_conn = engine.begin()
            self.conn = await self._engine_conn.__aenter__()
        else:
            self.conn = self._conn
        self._init_repos()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn is None:
            await self._engine_conn.__aexit__(exc_type, exc_val, exc_tb)

    def _init_repos(self):
        self.schedule_repo = ScheduleRepository(self.conn)
        self.date_register_repo = DateRegisterRepository(self.conn)
        self.category_repo = CategoryRepository(self.conn)

    async def add_category(self, category: CategoryCreate) -> Category:
        return await self.category_repo.create(category)

    async def add_date_record(self, register: DateRegisterCreate) -> DateRegister:
        return await self.date_register_repo.create(register)

    async def add_schedule(self, routine: ScheduledRoutineCreate) -> ScheduledRoutine:
        return await self.schedule_repo.create(routine)

    async def get_records_for_relationship(self, relationship_field: str) -> List[DateRegister]:
        return await self.date_register_repo.get_by_relationship(relationship_field)

    async def get_records_for_schedule(self, schedule_id: UUID) -> List[DateRegister]:
        return await self.date_register_repo.get_by_schedule(schedule_id)

    async def get_dates_from_range(self, start: datetime, end: datetime) -> List[DateRegister]:
        return await self.date_register_repo.get_dates_from_range(start, end)
