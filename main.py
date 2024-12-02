import re
import smtplib
from aiogram import Bot, Dispatcher, executor, types
from config import load_config

config = load_config()

BOT_TOKEN = config["token"]

YANDEX_SMTP_SERVER = config["smtp_server"]
YANDEX_SMTP_PORT = config["smtp_port"]
YANDEX_EMAIL = config["email"]
YANDEX_PASSWORD = config["password"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регулярное выражение для проверки email
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

user_states = {}

# Хендлер для команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_states[message.from_user.id] = {"email": None, "text": None}
    await message.reply("Привет! Пожалуйста, введите ваш email.")

# Хендлер для получения email
@dp.message_handler(lambda message: user_states.get(message.from_user.id, {}).get("email") is None)
async def get_email(message: types.Message):
    email = message.text.strip()
    if re.match(EMAIL_REGEX, email):
        user_states[message.from_user.id]["email"] = email
        await message.reply("Email принят! Теперь напишите текст сообщения.")
    else:
        await message.reply("Это некорректный email. Попробуйте снова.")

# Хендлер для получения текста сообщения
@dp.message_handler(lambda message: user_states.get(message.from_user.id, {}).get("email") is not None and user_states[message.from_user.id].get("text") is None)
async def get_message_text(message: types.Message):
    text = message.text.strip()
    user_states[message.from_user.id]["text"] = text
    email = user_states[message.from_user.id]["email"]
    
    try:
        # Отправляем email через SMTP
        send_email(email, text)
        await message.reply("Сообщение отправлено на ваш email!")
    except Exception as e:
        await message.reply(f"Произошла ошибка при отправке письма: {e}")
    finally:
        user_states.pop(message.from_user.id, None)  # Сбрасываем состояние пользователя

def send_email(to_email, message_text):
    """Отправляет письмо через SMTP"""
    with smtplib.SMTP(YANDEX_SMTP_SERVER, YANDEX_SMTP_PORT) as server:
        server.starttls()  # Используем TLS
        server.login(YANDEX_EMAIL, YANDEX_PASSWORD)
                
        subject = "Сообщение из Telegram-бота"
        headers = f"From: {YANDEX_EMAIL}\r\nTo: {to_email}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n"
        
        # Кодируем текст сообщения в UTF-8
        message = headers + "\r\n" + message_text
                
        server.sendmail(YANDEX_EMAIL, to_email, message.encode('utf-8'))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
