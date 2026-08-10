# Task Tracker API

Учебный pet-проект: backend трекера задач на FastAPI. Пользователи регистрируются, заводят проекты, создают в них задачи, назначают исполнителей и вешают теги. Написан как практический проект в рамках роадмапа Python Backend Developer (Phase 3 — FastAPI и REST API).

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL-совместимый SQL через SQLAlchemy 2.0 (async)** — сейчас база SQLite (`aiosqlite`), схема ORM не завязана на конкретную СУБД
- **Alembic** — миграции схемы БД
- **Pydantic v2 / pydantic-settings** — валидация данных и конфиг через `.env`
- **AuthX (JWT в cookie) + passlib/bcrypt** — аутентификация и хранение паролей
- **pytest + pytest-asyncio + httpx** — тесты (43 теста, все запросы идут через реальный ASGI-стек в изолированную тестовую БД)

## Возможности

- Регистрация / логин / текущий пользователь (`/auth/*`), JWT в httpOnly-cookie, CSRF-защита на изменяющих запросах
- Проекты: создание, список (с пагинацией), чтение, обновление, удаление — доступ только у владельца
- Задачи внутри проекта: создание, список (пагинация + фильтры по статусу и исполнителю), чтение, обновление (включая переназначение исполнителя), удаление — доступ у владельца проекта
- Теги: общий список тегов, привязка/отвязка тега к задаче (many-to-many)
- Логирование каждого запроса (метод, путь, код ответа, время выполнения)

## Структура проекта

```
src/
  core/
    config.py        — настройки из .env (pydantic-settings)
    db_core.py        — async engine, сессии, Base
    security/          — хэширование паролей, JWT (AuthX)
  models/
    Models.py          — SQLAlchemy-модели (Users, Projects, Tasks, Tags, TaskTags)
  schemas/              — Pydantic-схемы (Create/Read/Update на каждую сущность)
  crud/                 — бизнес-логика и доступ к БД
  routers/              — эндпоинты FastAPI
  main.py               — сборка приложения, middleware логирования
alembic/                — миграции
test/
  conftest.py           — фикстуры: изолированная тестовая БД, HTTP-клиент, авторизованные пользователи
  crud/                 — юнит-тесты на CRUD-слой напрямую
  route/                — интеграционные тесты через HTTP (основной набор)
```

## Как запустить

1. Клонировать репозиторий, создать и активировать venv в корне проекта:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Поставить зависимости:
   ```bash
   pip install "fastapi[standard]" sqlalchemy aiosqlite alembic pydantic-settings authx passlib bcrypt pytest pytest-asyncio httpx
   ```
3. Скопировать `.env.example` в `.env` и задать свой `JWT_SECRET_KEY` (случайную строку, не значение из примера):
   ```bash
   cp .env.example .env
   ```
4. Применить миграции:
   ```bash
   alembic upgrade head
   ```
5. Запустить сервер (из корня проекта, не из `src/`):
   ```bash
   fastapi dev src/main.py
   ```
6. Swagger-документация — `http://127.0.0.1:8000/docs`.

## Тесты

```bash
pytest test/ -v
```
Тесты используют отдельную in-memory/файловую SQLite-базу (`DATABASE_URL_TEST` из `.env`), реальная `task_tracker.db` не затрагивается.

## API

| Метод | Путь | Описание |
|---|---|---|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Логин, выдаёт JWT |
| GET | `/auth/me` | Текущий пользователь |
| POST | `/projects/` | Создать проект |
| GET | `/projects/all` | Список своих проектов (`limit`/`offset`) |
| GET | `/projects/{id}` | Получить проект |
| PUT | `/projects/{id}` | Обновить проект |
| DELETE | `/projects/{id}` | Удалить проект |
| POST | `/tasks/?project_id=` | Создать задачу в проекте |
| GET | `/tasks/all?project_id=` | Список задач проекта (`limit`/`offset`, `status`, `assignee_id`) |
| GET | `/tasks/{id}` | Получить задачу |
| PUT | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |
| POST | `/tasks/{id}/tags/{tag_id}` | Привязать тег к задаче |
| DELETE | `/tasks/{id}/tags/{tag_id}` | Отвязать тег от задачи |
| GET | `/tags/` | Список всех тегов |
| POST | `/tags/` | Создать тег |

Все эндпоинты, кроме `register`/`login`, требуют авторизации (JWT в cookie). Для `POST`/`PUT`/`DELETE` дополнительно нужен заголовок `X-CSRF-Token` со значением claim `csrf` из токена (защита от CSRF при аутентификации через cookie).
