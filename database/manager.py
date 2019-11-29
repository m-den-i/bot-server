import settings

from .db import DatabaseManager

database_manager = DatabaseManager(settings.DATABASE_CONNECTION_URL)
