import asyncio
from datetime import UTC, datetime

from app.core.database import async_session_factory
from app.core.security import hash_password
from app.models.department import Department
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.models.position import Position
from sqlalchemy import select


async def seed() -> None:
    async with async_session_factory() as session:
        # -------------------------
        # Departments
        # -------------------------

        departments_data = [
            {
                "name": "IT",
                "description": "Information Technology Department",
            },
            {
                "name": "HR",
                "description": "Human Resources Department",
            },
            {
                "name": "Finance",
                "description": "Finance Department",
            },
            {
                "name": "Marketing",
                "description": "Marketing Department",
            },
        ]

        departments: dict[str, Department] = {}

        for data in departments_data:
            result = await session.execute(
                select(Department).where(Department.name == data["name"])
            )

            department = result.scalar_one_or_none()

            if department is None:
                department = Department(**data)
                session.add(department)

            departments[data["name"]] = department

        # -------------------------
        # Positions
        # -------------------------

        positions_data = [
            {
                "name": "Frontend Developer",
                "description": "Develops frontend applications.",
            },
            {
                "name": "Backend Developer",
                "description": "Develops backend services and APIs.",
            },
            {
                "name": "Fullstack Developer",
                "description": "Develops frontend and backend applications.",
            },
            {
                "name": "HR Manager",
                "description": "Manages HR processes and employees.",
            },
            {
                "name": "Accountant",
                "description": "Manages financial records and accounting.",
            },
        ]

        positions: dict[str, Position] = {}

        for data in positions_data:
            result = await session.execute(
                select(Position).where(Position.name == data["name"])
            )

            position = result.scalar_one_or_none()

            if position is None:
                position = Position(**data)
                session.add(position)

            positions[data["name"]] = position

        # Flush so newly created departments and positions
        # receive their database IDs.
        await session.flush()

        # -------------------------
        # Admin
        # -------------------------

        admin_email = "admin@corporate.com"

        result = await session.execute(
            select(Employee).where(Employee.email == admin_email)
        )

        admin = result.scalar_one_or_none()

        if admin is None:
            admin = Employee(
                email=admin_email,
                password_hash=hash_password("Admin123!"),
                first_name="System",
                last_name="Administrator",
                hire_date=datetime.now(UTC).date(),
                department_id=departments["IT"].id,
                position_id=positions["Fullstack Developer"].id,
                role=EmployeeRole.ADMIN,
                is_active=True,
            )

            session.add(admin)

        await session.commit()

        print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
