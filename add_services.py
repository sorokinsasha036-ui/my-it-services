from project_db import init_db, SessionLocal, Service


services = [
    {
        "name": "Веб-розробка",
        "description": "Створення сучасних вебсайтів, інтернет-магазинів, вебзастосунків та адміністративних панелей.",
        "price": 5000,
        "category": "Веб-розробка",
    },
    {
        "name": "Розробка програмного забезпечення",
        "description": "Створення програм, backend-систем, REST API та індивідуальних програмних рішень.",
        "price": 7000,
        "category": "Програмне забезпечення",
    },
    {
        "name": "Telegram-боти",
        "description": "Розробка Telegram-ботів для бізнесу, автоматизації, замовлень та взаємодії з користувачами.",
        "price": 3000,
        "category": "Telegram",
    },
    {
        "name": "Автоматизація",
        "description": "Автоматизація рутинних операцій, обробки даних, web scraping та інтеграції різних сервісів.",
        "price": 4000,
        "category": "Автоматизація",
    },
    {
        "name": "AI-рішення",
        "description": "Інтеграція можливостей штучного інтелекту у вебсайти, програми, ботів та автоматизовані системи.",
        "price": 5000,
        "category": "AI",
    },
    {
        "name": "Підтримка та доопрацювання",
        "description": "Виправлення помилок, додавання нових функцій, оптимізація та технічна підтримка існуючих проєктів.",
        "price": 1500,
        "category": "Підтримка",
    },
]


def seed_services():
    init_db()
    db = SessionLocal()

    try:
        existing_names = {
            name
            for (name,) in db.query(Service.name).all()
        }

        added = 0
        skipped = 0

        for data in services:
            if data["name"] in existing_names:
                skipped += 1
                continue

            db.add(Service(**data))
            existing_names.add(data["name"])
            added += 1

        db.commit()

        print(f"Додано нових послуг: {added}")
        print(f"Вже існувало: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_services()