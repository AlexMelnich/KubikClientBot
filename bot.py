import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Токен бота (замени на свой)
TOKEN = "7415616893:AAHRkS39SJbbPFOcjmkfZzTRX9jsmTQfpOE"

# Список прайс-листов
price_lists = {
    "Пазлы Melograno": "https://disk.yandex.ru/i/uR4R6bj5FBYGzA",
    "1Toy": "https://disk.yandex.ru/d/lQcrerEHc-heWA",
    "Zuru": "https://disk.yandex.ru/d/G5Lp27zTCXvnAw",
    "Мягкая игрушка Мишуткин": "https://disk.yandex.ru/d/aVMVSVpNwo7VsQ",
    "Игрушки для малышей": "https://disk.yandex.ru/d/gNTngFE4j7Hv5A",
    "Деревянные игрушки": "https://disk.yandex.ru/d/OKasHwlIigB2GQ"
}

# Логирование
logging.basicConfig(level=logging.WARNING)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Генерация клавиатуры с кнопками брендов
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text=brand)] for brand in price_lists.keys()])
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Выберите бренд, чтобы получить прайс:", reply_markup=get_keyboard())

# Обработчик кнопок с брендами
@dp.message()
async def send_price(message: types.Message):
    if message.text in price_lists:
        brand = message.text
        await message.answer(f"📄 Прайс {brand}: {price_lists[brand]}")

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
