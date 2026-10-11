import os

from werkzeug.security import generate_password_hash

from project_db import init_db, SessionLocal, User


username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if not username or not email or not password:
    raise RuntimeError(
        "Set ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD."
    )

# Переконуємося, що таблиці створені.
init_db()

db = SessionLocal()

try:
    # Шукаємо адміністратора за email.
    admin = db.query(User).filter_by(email=email).first()

    if admin:
        # Оновлюємо обліковий запис адміністратора.
        admin.username = username
        admin.password_hash = generate_password_hash(password)
        admin.role = "admin"

        print("Admin account updated.")
    else:
        # Перевіряємо, чи зайняте ім'я користувача.
        existing_user = (
            db.query(User)
            .filter_by(username=username)
            .first()
        )

        if existing_user:
            raise RuntimeError(
                "This username belongs to another account."
            )

        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="admin",
        )

        db.add(admin)
        print("Admin account created.")

    db.commit()

except Exception:
    db.rollback()
    raise

finally:
    db.close()