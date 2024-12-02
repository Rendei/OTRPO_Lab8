# Телеграм-бот для отправки писем через SMTP Яндекса

Этот проект реализует телеграм-бота, который запрашивает у пользователя адрес электронной почты и текст сообщения, проверяет валидность email и отправляет сообщение на указанный адрес с использованием SMTP сервера Яндекса.

## Возможности
- Запрашивает и проверяет email пользователя.
- Принимает текст сообщения для отправки.
- Отправляет сообщение на указанный email через `smtplib` и SMTP Яндекса.


## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Rendei/telegram-email-bot.git
   cd telegram-email-bot
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `config.json` в папке проекта и добавьте следующие переменные окружения:
   ```env
    {
        "token": "your_token",
        "smtp_server": "smtp.yandex.com",
        "smtp_port": 587,
        "email": "your_email",
        "password": "your_password"
    }
   ```

   Замените плейсхолдеры на ваши реальные данные.

5. Убедитесь, что в вашем аккаунте Яндекса включены [пароли для приложений](https://yandex.ru/support/id/authorization/app-passwords.html) для доступа к SMTP.

## Использование

1. Запустите бота:
   ```bash
   python main.py
   ```

2. Откройте Телеграм и найдите вашего бота.

3. Начните диалог с командой `/start`:
   - Бот запросит ваш email.
   - Проверит правильность формата email.
   - После проверки запросит текст сообщения.
   - Отправит сообщение на указанный email.

4. После успешной отправки бот подтвердит это сообщением.

## Структура проекта
```
├── main.py          # Основная логика бота
├── config.py        # Загрузка конфига
├── requirements.txt # Зависимости проекта
├── README.md        # Документация проекта
```

## Зависимости
- **[aiogram](https://docs.aiogram.dev/)**: Фреймворк для создания телеграм-ботов.
- **[smtplib](https://docs.python.org/3/library/smtplib.html)**: Для отправки писем через SMTP Яндекса.
- **[re](https://docs.python.org/3/library/re.html)**: Для проверки валидности email.

## Настройки SMTP
Бот использует SMTP сервер Яндекса для отправки писем. Убедитесь, что:
- Вы включили "Доступ для менее защищённых приложений" или создали пароль для приложений в аккаунте Яндекса.
- Указаны правильные настройки сервера:
  - Сервер: `smtp.yandex.com`
  - Порт: `587`

## Пример работы
```plaintext
Пользователь: /start
Бот: Привет! Пожалуйста, введите ваш email.
Пользователь: example@yandex.ru
Бот: Email принят! Теперь напишите текст сообщения.
Пользователь: Привет, это тестовое сообщение!
Бот: Сообщение отправлено на ваш email!
```

## Обработка ошибок
- Некорректный формат email вызывает повторный запрос.
- Ошибки SMTP обрабатываются и сообщаются пользователю.