from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.store.database import db
from app.store.database.database_url import DATABASE_URL

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        url = f"postgresql+asyncpg://{self.app.config.database.user}:{self.app.config.database.password}@{self.app.config.database.host}:{self.app.config.database.port}/{self.app.config.database.database}"
        self._engine = create_async_engine(url, echo=True, future=True)
        self.session = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )
        self.app.logger.info("Database connected")

    async def disconnect(self, *_: list, **__: dict) -> None:
        self.app.logger.info("Database disconnected")
