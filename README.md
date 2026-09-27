# LibraryApp — Онлайн-библиотека

Учебный Django-проект, разработанный в рамках курса CSE8272. Онлайн-каталог книг с поиском, формами, медиафайлами и JSON API.

---

## Назначение и целевая аудитория

Онлайн-библиотека предназначена для ведения каталога книг: добавления, редактирования и просмотра записей. Целевая аудитория — студенты и читатели, которым нужен простой инструмент для учёта книжного фонда.

---

## Стек технологий

| Компонент       | Технология                     |
|-----------------|-------------------------------|
| Backend         | Python 3.13, Django 6.1        |
| База данных     | SQLite (файл `db.sqlite3`)     |
| Шаблоны         | Django Template Language (DTL) |
| Frontend        | HTML5, CSS3 (CSS Variables), JavaScript (Vanilla) |
| Медиафайлы      | Pillow, Django Media Files     |
| API             | Django JsonResponse (без DRF)  |

---

## Установка и запуск

### Требования
- Python 3.10+
- pip

### Шаги

```bash
# 1. Клонировать репозиторий
git clone <url>
cd CSE8272onl

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Перейти в папку проекта
cd library_projectcd lib  

# 4. Применить миграции
python manage.py migrate

# 5. Заполнить базу тестовыми данными
python manage.py seed

# 6. Создать суперпользователя (для admin-панели)
python manage.py createsuperuser

# 7. Запустить сервер
python manage.py runserver
```

Сайт будет доступен по адресу: **http://127.0.0.1:8000/**

Данные для входа в admin (если использовалась команда seed + --noinput):
- Логин: `admin`
- Пароль: задаётся при `createsuperuser`

---

## Основные URL

| URL                         | Описание                       |
|-----------------------------|-------------------------------|
| `/`                         | Главная страница, последние книги |
| `/catalog/`                 | Каталог всех книг              |
| `/catalog/?q=dune`          | Поиск по названию/автору       |
| `/catalog/?category=fiction`| Фильтр по категории            |
| `/book/<id>/`               | Детальная страница книги       |
| `/book/add/`                | Форма добавления книги         |
| `/book/<id>/edit/`          | Форма редактирования           |
| `/book/<id>/delete/`        | Подтверждение удаления         |
| `/admin/`                   | Django Admin                   |

---

## API

Базовый путь: `/api/`

### GET `/api/books/`

Возвращает список всех книг в формате JSON.

**Параметры запроса (опционально):**
- `?q=<текст>` — поиск по названию или автору
- `?category=<slug>` — фильтр по категории (slug: `fiction`, `science`, `history`)

**Пример ответа:**
```json
[
  {
    "id": 1,
    "title": "1984",
    "author": "George Orwell",
    "category": "Fiction",
    "year": 1949,
    "available": true
  }
]
```

### GET `/api/books/<id>/`

Возвращает детальную информацию об одной книге.

**Пример ответа:**
```json
{
  "id": 1,
  "title": "1984",
  "author": "George Orwell",
  "category": "Fiction",
  "description": "A dystopian novel set in a totalitarian state...",
  "year": 1949,
  "available": true,
  "cover_url": "/media/covers/1984.jpg"
}
```

**Ошибка (книга не найдена):**
```json
{"error": "Not found"}
```
HTTP статус: `404`

---

## Схема моделей

```
Author
  - id (PK)
  - name (CharField)
  - bio (TextField, необязательное)

Category
  - id (PK)
  - name (CharField)
  - slug (SlugField, уникальный)

Book
  - id (PK)
  - title (CharField)
  - author → Author (FK, CASCADE)
  - category → Category (FK, SET_NULL, необязательное)
  - description (TextField, необязательное)
  - cover (ImageField, необязательное, папка covers/)
  - year (PositiveIntegerField, необязательное)
  - available (BooleanField, по умолчанию True)
  - created_at (DateTimeField, auto_now_add)
```

**Связи:** один автор может иметь много книг; одна категория может содержать много книг.

---

## Использование ИИ (LLM)

При разработке проекта использовался Claude Sonnet 4.6 (Anthropic) в роли инструмента-ассистента:
- **Генерация кода:** шаблоны Django, CSS, JavaScript, views, models, forms
- **Структура проекта:** рекомендации по организации файлов и URL-схеме
- **Документация:** оформление README

Все сгенерированные фрагменты были проверены, скорректированы и интегрированы вручную студентом в соответствии с требованиями ТЗ.
