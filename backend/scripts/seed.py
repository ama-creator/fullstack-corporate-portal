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
            {
                "name": "Marketing Manager",
                "description": "Manages marketing activities and campaigns.",
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
        # Employees
        # -------------------------

        employees_data = [
            {
                "email": "admin@corporate.com",
                "password": "Admin123!",
                "first_name": "System",
                "last_name": "Administrator",
                "department": "IT",
                "position": "Fullstack Developer",
                "role": EmployeeRole.ADMIN,
                "is_active": True,
            },
            {
                "email": "alexey.smirnov@corporate.com",
                "password": "Employee123!",
                "first_name": "Alexey",
                "last_name": "Smirnov",
                "department": "IT",
                "position": "Backend Developer",
                "role": EmployeeRole.EMPLOYEE,
                "is_active": True,
            },
            {
                "email": "anna.volkova@corporate.com",
                "password": "Employee123!",
                "first_name": "Anna",
                "last_name": "Volkova",
                "department": "IT",
                "position": "Frontend Developer",
                "role": EmployeeRole.EMPLOYEE,
                "is_active": True,
            },
            {
                "email": "mikhail.petrov@corporate.com",
                "password": "Employee123!",
                "first_name": "Mikhail",
                "last_name": "Petrov",
                "department": "IT",
                "position": "Fullstack Developer",
                "role": EmployeeRole.MANAGER,
                "is_active": True,
            },
            {
                "email": "elena.sokolova@corporate.com",
                "password": "Employee123!",
                "first_name": "Elena",
                "last_name": "Sokolova",
                "department": "HR",
                "position": "HR Manager",
                "role": EmployeeRole.HR,
                "is_active": True,
            },
            {
                "email": "olga.morozova@corporate.com",
                "password": "Employee123!",
                "first_name": "Olga",
                "last_name": "Morozova",
                "department": "Finance",
                "position": "Accountant",
                "role": EmployeeRole.EMPLOYEE,
                "is_active": True,
            },
            {
                "email": "sergey.ivanov@corporate.com",
                "password": "Employee123!",
                "first_name": "Sergey",
                "last_name": "Ivanov",
                "department": "Finance",
                "position": "Accountant",
                "role": EmployeeRole.MANAGER,
                "is_active": True,
            },
            {
                "email": "dmitry.kuznetsov@corporate.com",
                "password": "Employee123!",
                "first_name": "Dmitry",
                "last_name": "Kuznetsov",
                "department": "IT",
                "position": "Backend Developer",
                "role": EmployeeRole.EMPLOYEE,
                "is_active": False,
            },
            {
                "email": "maria.orlova@corporate.com",
                "password": "Employee123!",
                "first_name": "Maria",
                "last_name": "Orlova",
                "department": "Marketing",
                "position": "Marketing Manager",
                "role": EmployeeRole.MANAGER,
                "is_active": True,
            },
        ]

        for data in employees_data:
            result = await session.execute(
                select(Employee).where(Employee.email == data["email"])
            )

            employee = result.scalar_one_or_none()

            if employee is None:
                employee = Employee(
                    email=data["email"],
                    password_hash=hash_password(data["password"]),
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    hire_date=datetime.now(UTC).date(),
                    department_id=departments[data["department"]].id,
                    position_id=positions[data["position"]].id,
                    role=data["role"],
                    is_active=data["is_active"],
                )

                session.add(employee)

        await session.commit()

        await session.commit()

        print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
