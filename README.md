# tg_bot_for_x_restaurant

/project
  |-- bot/                     # Основная логика бота
  |     |-- handlers/          # Хендлеры для обработки команд и сообщений
  |     |     |-- admin/       # Хендлеры для админских функций
  |     |     |     |-- orders.py          # Управление заказами
  |     |     |     |-- menu.py            # Управление меню (блюда и категории)
  |     |     |     |-- notifications.py   # Уведомления пользователям
  |     |     |     |-- stats.py           # Статистика заказов
  |     |     |-- user/        # Хендлеры для пользовательских функций
  |     |           |-- start.py           # Команда /start и регистрация
  |     |           |-- menu.py            # Просмотр меню
  |     |           |-- orders.py          # Оформление и просмотр заказов
  |     |-- keyboards/         # Клавиатуры (Inline и Reply)
  |     |     |-- admin_keyboards.py       # Клавиатуры для админов
  |     |     |-- user_keyboards.py        # Клавиатуры для пользователей
  |     |-- middlewares/       # Миддлвары для управления запросами
  |     |     |-- auth_middleware.py       # Проверка на администратора
  |     |-- states/            # FSM состояния (Finite State Machine)
  |     |     |-- registration.py          # Состояния для регистрации
  |     |     |-- add_dish.py              # Состояния для добавления блюд
  |     |     |-- notify.py                # Состояния для уведомлений
  |     |-- utils/             # Утилиты (помощники)
  |           |-- db.py                    # Функции для работы с БД
  |           |-- validators.py            # Валидация данных
  |           |-- misc.py                  # Прочие утилиты
  |-- static/                  # Статические файлы
  |     |-- images/            # Фотографии блюд
  |          |-- dishes/       # Каталог для хранения изображений блюд
  |-- database/                # Логика работы с базой данных
  |     |-- models.py          # SQL-запросы и функции для взаимодействия с таблицами
  |     |-- migrations/        # Миграции для базы данных
  |-- config.py                # Конфигурация приложения (настройки, токены)
  |-- main.py                  # Точка входа в приложение
  |-- README.md                # Документация
  |-- requirements.txt         # Список зависимостей
