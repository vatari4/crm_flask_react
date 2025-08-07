from app.models.user import User, Role
from app.auth.auth_service import hash_password
from app.db.database import db
from datetime import date
from app.models.analytics import (
    UserAnalytics, ContractAnalytics, DealAnalytics,
    TopEmployee, PerformanceAnalytics, AnalyticsMetadata
)


def create_roles_if_not_exist():
    role_names = ["Администратор", "Мэнеджер", "Сис-админ", "Кассир"]
    roles = {}

    for name in role_names:
        role = db.session.query(Role).filter_by(name=name).first()
        if not role:
            role = Role(name=name)
            db.session.add(role)
            print(f"✅ Created role: {name}")
        roles[name] = role

    db.session.commit()
    return roles


def create_default_users():
    roles = create_roles_if_not_exist()

    users_data = [
        {
            "username": "Виктор", "password": "1", "role": "Администратор",
            "first_name": "Виктор", "last_name": "Петров", "middle_name": "Иванович",
            "employment_start_date": date(2020, 1, 10),
            "employment_end_date": None,
        },
        {
            "username": "Аня", "password": "12", "role": "Мэнеджер",
            "first_name": "Анна", "last_name": "Смирнова", "middle_name": "Александровна",
            "employment_start_date": date(2021, 5, 20),
            "employment_end_date": None,
        },
        {
            "username": "Вася", "password": "13", "role": "Сис-админ",
            "first_name": "Василий", "last_name": "Иванов", "middle_name": "Петрович",
            "employment_start_date": date(2019, 11, 1),
            "employment_end_date": None,
        },
        {
            "username": "Иван", "password": "14", "role": "Кассир",
            "first_name": "Иван", "last_name": "Соколов", "middle_name": "Дмитриевич",
            "employment_start_date": date(2022, 3, 15),
            "employment_end_date": None,
        },
    ]

    created_users = {}

    for user_data in users_data:
        user = db.session.query(User).filter_by(username=user_data["username"]).first()
        if not user:
            user = User(
                username=user_data["username"],
                password=hash_password(user_data["password"]),
                role=roles[user_data["role"]],
                manager_id=None,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                middle_name=user_data["middle_name"],
                employment_start_date=user_data["employment_start_date"],
                employment_end_date=user_data["employment_end_date"],
            )
            db.session.add(user)
            db.session.flush()
            print(f"✅ Created user: {user.username} / {user_data['password']}")
        created_users[user_data["username"]] = user

    admin_user = created_users.get("Виктор")
    for username, user in created_users.items():
        if user.role.name != "Администратор" and user.manager_id != admin_user.id:
            user.manager_id = admin_user.id
            print(f"🔁 Updated {username}: manager = {admin_user.username}")

    # Вычисляем и записываем срок службы в днях
    for user in created_users.values():
        if user.employment_start_date:
            end_date = user.employment_end_date or date.today()
            user.service_duration_days = (end_date - user.employment_start_date).days
        else:
            user.service_duration_days = 0

    db.session.commit()
    print("✅ All default users created and manager assigned")


def create_default_analytics():
    users = db.session.query(User).all()

    for user in users:
        if not db.session.query(UserAnalytics).filter_by(user_id=user.id).first():
            db.session.add(UserAnalytics(
                user_id=user.id,
                total_visitors=100 + user.id * 10,
                new_visitors=50 + user.id * 5,
                returning_visitors=30 + user.id * 2
            ))

        if not db.session.query(ContractAnalytics).filter_by(user_id=user.id).first():
            db.session.add(ContractAnalytics(
                user_id=user.id,
                in_progress=3 + user.id,
                signed=5 + user.id,
                total=10 + user.id,
                rejected=2
            ))

        if not db.session.query(DealAnalytics).filter_by(user_id=user.id).first():
            db.session.add(DealAnalytics(
                user_id=user.id,
                deals_count=10 + user.id,
                revenue=10000.0 + user.id * 1000
            ))

        if not db.session.query(TopEmployee).filter_by(user_id=user.id).first():
            top_employee = TopEmployee(
                user_id=user.id,
                name=f"{user.last_name} {user.first_name} {user.middle_name}",
                department="Sales" if user.role.name == "Мэнеджер" else "Support",
                kpi=75.5 + user.id,
                deals_closed=12 + user.id,
                revenue_generated=50000 + user.id * 1000
            )
            db.session.add(top_employee)
            db.session.flush()

            db.session.add(PerformanceAnalytics(
                top_employee_id=top_employee.id,
                team_average=70.0 + user.id
            ))

    if not db.session.query(AnalyticsMetadata).first():
        db.session.add(AnalyticsMetadata(
            period="Май 2025",
            generated_at="2025-06-01 12:00:00",
            source="Автоматический сбор данных"
        ))

    db.session.commit()
    print("✅ Default analytics data created")


if __name__ == "__main__":
    create_default_users()
    create_default_analytics()
