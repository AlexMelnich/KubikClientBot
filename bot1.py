import asyncio
import json
import random
import string
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

# Вставьте ваш токен бота
API_TOKEN = "7415616893:AAHRkS39SJbbPFOcjmkfZzTRX9jsmTQfpOE"
CHANNEL_ID = "-1002282076022"  # ID канала в формате -100XXXXXXXXXX
PROMO_FILE = "promo_codes.json"  # Файл для хранения промокодов
PROMO_VALIDITY_DAYS = 30  # Срок действия промокода в днях

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_promo_codes():
    """Загрузка промокодов из файла. Если файл поврежден — создаем новый."""
    try:
        with open(PROMO_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Ошибка загрузки promo_codes.json! Создаем новый файл...")
        return {}

def save_promo_codes(promo_codes):
    """Сохранение промокодов в файл."""
    with open(PROMO_FILE, "w", encoding="utf-8") as file:
        json.dump(promo_codes, file, indent=4, ensure_ascii=False)

def generate_promo_code():
    """Генерация уникального промокода."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

async def check_subscription(user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал."""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        return False  # Если бот не может получить статус, считаем, что не подписан

@dp.message()
async def handle_message(message: Message):
    """Обрабатывает сообщения и выдает уникальный промокод."""
    if message.text == "/start":
        user_id = str(message.from_user.id)
        promo_codes = load_promo_codes()

        if user_id in promo_codes and isinstance(promo_codes[user_id], dict):
            promo_code = promo_codes[user_id]["code"]
            expiration_date = promo_codes[user_id]["expires"]
            await message.answer(
                f"✅ Вы уже получали промокод: **{promo_code}**\n"
                f"📅 Он действителен до **{expiration_date}**\n"
                "🎁 Надеемся, вы сделали заказ с дополнительной скидкой!"
            )
        else:
            await asyncio.sleep(2)  # Добавляем задержку для обновления статуса подписки
            is_subscribed = await check_subscription(message.from_user.id)

            if is_subscribed:
                new_promo = generate_promo_code()
                expiration_date = (datetime.date.today() + datetime.timedelta(days=PROMO_VALIDITY_DAYS)).strftime("%d.%m.%Y")
                promo_codes[user_id] = {"code": new_promo, "expires": expiration_date}
                save_promo_codes(promo_codes)

                await message.answer(
                    f"✅ Спасибо за подписку! Ваш уникальный промокод: **{new_promo}**\n"
                    f"📅 Он действителен до **{expiration_date}**!"
                )
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔗 Подписаться на канал", url=f"https://t.me/kubik_opt")]
                ])
                await message.answer(
                    "❌ Вы не подписаны на наш канал!\n"
                    "👉 Подпишитесь на @kubik_opt и попробуйте снова через несколько секунд!",
                    reply_markup=keyboard
                )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

