# tg_bot_for_x_restaurant

```
project/
├── bot/
│   ├── __init__.py
│   ├── main.py               # Точка входа для запуска бота
│   ├── config.py             # Конфигурация бота
│   ├── handlers/             # Основные обработчики
│   │   ├── admin/            # Обработчики для администраторов
│   │   │   ├── __init__.py
│   │   │   ├── menu_management.py  # Управление меню
│   │   │   ├── order_management.py # Управление заказами
│   │   │   ├── promo_codes.py      # Работа с промокодами
│   │   │   ├── staff_management.py # Управление персоналом
│   │   │   ├── stats.py          # Генерация отчетов
│   │   ├── user/             # Обработчики для пользователей
│   │       ├── __init__.py
│   │       ├── start.py            # Регистрация и начальный экран
│   │       ├── menu.py             # Просмотр меню
│   │       ├── orders.py           # Управление заказами
│   │       ├── settings.py         # Пользовательские настройки
│   │       ├── reviews.py          # Отправка отзывов
│   ├── keyboards/            # Клавиатуры
│   │   ├── __init__.py
│   │   ├── common.py         # Общие клавиатуры
│   │   ├── admin_keyboards.py          # Клавиатуры для админов
│   │   ├── user_keyboards.py           # Клавиатуры для пользователей
│   ├── states/               # Машины состояний (FSM)
│   │   ├── __init__.py
│   │   ├── admin.py          # FSM для админов
│   │   ├── user.py           # FSM для пользователей
│   ├── middlewares/          # Миддлвары
│   │   ├── __init__.py
│   │   ├── language.py       # Миддлвар для выбора языка
│   │   ├── role_check.py     # Проверка роли пользователя
│   ├── services/             # Сервисы
│   │   ├── __init__.py
│   │   ├── database.py       # Работа с базой данных
│   │   ├── sms.py            # Сервис отправки SMS
│   │   ├── order_processing.py # Общая логика заказов
│   │   ├── menu_service.py   # Логика управления меню
│   ├── utils/                # Утилиты
│       ├── __init__.py
│       ├── validators.py     # Валидация данных
│       ├── notifications.py  # Уведомления для пользователей и админов
├── migrations/               # Миграции базы данных
├── tests/                    # Тесты
├── requirements.txt          # Зависимости проекта
├── Dockerfile                # Docker-контейнер
├── docker-compose.yml        # Конфигурация Docker Compose
├── README.md                 # Документация проекта

```
