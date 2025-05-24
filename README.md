# Backend — Mental Health Platform

Это серверная часть проекта стартапа, разработанная на Flask. Система поддерживает:

- Регистрацию и авторизацию пользователей
- Роли (user, admin, superadmin)
- Сохранение и выдачу результатов психологических тестов
- Аудит действий пользователей (activity log)
- Загрузку аватара и смену темы
- Поддержку смены пароля через email

---

## Необходимые библиотеки

Установите зависимости с помощью `pip`:

```
pip install -r requirements.txt
```

---

Если у вас нет файла requirements.txt, создайте его вручную:
```
Flask
Flask-SQLAlchemy
Flask-Mail
python-dotenv
Flask-Cors
Werkzeug
```

---

Настройка
Перед запуском создайте файл .env в корне проекта со следующими переменными:
```
FLASK_APP=run.py
FLASK_ENV=development

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

DATABASE_URL=sqlite:///db.sqlite3  # или другой URL вашей базы данных
```
Важно: Для Gmail используйте пароль приложения, если у вас включена двухфакторная аутентификация.
---

Запуск
```
flask run
```
---

Структура проекта:
```
backend_server/
├── models.py          # SQLAlchemy-модели
├── routes/
│   └── auth.py        # Основные маршруты (регистрация, вход и пр.)
├── utils/
│   └── mail.py        # Отправка писем
├── static/uploads/    # Папка для аватаров
└── run.py             # Точка входа

```
---
Поддержка API
```
| Маршрут                   | Метод | Описание                          |
| ------------------------- | ----- | --------------------------------- |
| `/auth/register`          | POST  | Регистрация                       |
| `/auth/login`             | POST  | Вход                              |
| `/auth/profile`           | GET   | Получение профиля                 |
| `/auth/profile`           | PUT   | Обновление профиля                |
| `/auth/profile/upload`    | POST  | Загрузка аватара                  |
| `/auth/save-test-result`  | POST  | Сохранение результата теста       |
| `/auth/admin/users`       | GET   | Список всех пользователей (админ) |
| `/auth/admin/action-logs` | GET   | Журнал действий (админ)           |

```
