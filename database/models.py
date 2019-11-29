from typing import Dict, List

from sqlalchemy import Column, Integer, String, insert, update, select, column, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base

from database.manager import database_manager

Base = declarative_base()
databases_instance = database_manager.db


class AbstractModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @classmethod
    async def async_insert(cls, values: List[Dict[str, object]]):
        query = insert(cls)

        return await databases_instance.execute_many(query=query, values=values)

    @classmethod
    async def async_update(cls, where_clauses: List[object], values: Dict[str, object]):
        query = update(cls)

        for clause in where_clauses:
            query = query.where(clause)

        return await databases_instance.execute(query=query, values=values)

    @classmethod
    async def async_find_by(cls, fields: List[str], where_clauses: List[object]) -> List[object]:
        query = select([column(f) for f in fields])

        for clauses in where_clauses:
            query = query.where(clauses)

        items = await databases_instance.fetch_all(query=query)

        return [cls(**dict(item)) for item in items]


class AbstractUser(AbstractModel):
    __abstract__ = True

    def is_anonymous(self) -> bool:
        return True


class User(AbstractUser):
    __tablename__ = 'users'
    profile_id = Column(String, unique=True, nullable=False)
    skype_id = Column(String, unique=True, nullable=False)
    email = Column(Integer, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    do_not_disturb = Column(Boolean, nullable=False, default=True)
    role = Column(Integer, default=0)

    USER_ROLE = 0
    ADMIN_ROLE = 1

    ROLES = {
        USER_ROLE: 'User',
        ADMIN_ROLE: 'Admin'
    }

    def is_anonymous(self):
        return False

    def is_user(self) -> bool:
        return self.role == self.USER_ROLE

    def is_admin(self) -> bool:
        return self.role == self.ADMIN_ROLE
