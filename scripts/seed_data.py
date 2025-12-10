"""Seed database with initial data."""

import asyncio
from uuid import uuid4

from app.infrastructure.database.base import AsyncSessionLocal
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.security.password_handler import PasswordHandler


async def seed_database() -> None:
    """Seed database with initial data."""
    password_handler = PasswordHandler()
    
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        
        # Check if admin user exists
        admin = await user_repo.get_by_email("admin@example.com")
        if admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            id=uuid4(),
            email="admin@example.com",
            username="admin",
            hashed_password=password_handler.hash_password("admin123"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True,
            role="admin",
        )
        
        await user_repo.create(admin_user)
        print("Admin user created successfully")
        print("Email: admin@example.com")
        print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(seed_database())

