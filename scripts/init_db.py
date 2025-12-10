"""Initialize database."""

import asyncio

from alembic.config import Config
from alembic import command

from app.config import settings


def init_database() -> None:
    """Initialize database with migrations."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.sync_database_url)
    
    print("Running database migrations...")
    command.upgrade(alembic_cfg, "head")
    print("Database initialized successfully")


if __name__ == "__main__":
    init_database()

