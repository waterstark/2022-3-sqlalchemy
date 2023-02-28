import typing

from sqlalchemy import insert, select, update
from hashlib import sha256

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> Admin | None:
        query = select(AdminModel).where(AdminModel.email == email)
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
        res = initial_result.scalar()
        return Admin(res.id, res.email, res.password) if res else None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = await self.get_by_email(email)
        if admin is None:
            query = insert(AdminModel).values(
                email=email, password=sha256(password.encode()).hexdigest()
            )
            async with self.app.database.session() as session:
                async with session.begin():
                    await session.execute(query)
                    initial_result = await session.execute(select(AdminModel))
            res = initial_result.scalar()
            return Admin(res.id, res.email, res.password)
