from aiogram.dispatcher.filters import Text
from bestchange_api import BestChange

from bestchange_listener import get_cots
from config import *
from aiogram import Bot, Dispatcher, executor, types
from binance_connect import start_listening
from keyboards import *
from States import StatesChange
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def main():
    executor.start_polling(dp)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в бота который сканирует Бестчендж и Бинанс, находя связки",
                         reply_markup=keyboard_main)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change'))
async def process_change(callback_query: types.CallbackQuery):
    regime = callback_query.data[7:]
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    if regime == "value":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новую рабочую сумму:")
        await state.set_state(StatesChange.STATE_VALUE)

    if regime == "min_spread":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новую минимальную доходность:")
        await state.set_state(StatesChange.STATE_SPREAD)
    if regime == "min_good":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новое количество минимально хороших комментариев:")
        await state.set_state(StatesChange.STATE_MIN_GOOD)
    if regime == "max_bad":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите максимальное количество плохих комментариев:")
        await state.set_state(StatesChange.STATE_MAX_BAD)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change'), state=StatesChange.STATE_EMPTY)
async def process_change1(callback_query: types.CallbackQuery):
    await process_change(callback_query)


@dp.message_handler(Text(equals="Настройки⚙️"))
async def parameters_get(message: types.Message):
    temp_text = "Настройки бота на сейчас:\n" \
                "Сумма для работы: {} USDT\n" \
                "Минимальная доходность: {}%\n" \
                "Минимальное кол-во положительных комментариев: {}\n" \
                "Максимальное кол-во отрицательных комментариев: {}"
    temp_text = temp_text.format(parameters["value"],
                                 parameters["min_spread"],
                                 parameters["min_good"],
                                 parameters["max_bad"])
    await message.answer(temp_text, reply_markup=keyboard_inline_properties)


@dp.message_handler(Text(equals="Обновить🔃"))
async def update_get(message: types.Message):
    await message.answer("Начинаю поиск связок, это займет около минуты")
    text = "Поиск завершен 😁"
    text_quote = "1. USDT->{}\n" \
                 "Покупка по маркету за: {}\n" \
                 "2. {}->{}\n" \
                 "Курс обмена: {} {} на {} {}\n" \
                 "Ссылка на обменник: {}\n" \
                 "3. {}->USDT\n" \
                 "Продажа по маркету: {}\n\n" \
                 "Итоговая сумма: {} USDT\n" \
                 "Процентный спред: {}%"

    cotirs = get_cots()
    if len(cotirs) == 0:
        text = "Не найдены связки 😥"
    else:
        for i in cotirs:
            await message.answer(text_quote.format(
                i['from'], i['buy'],
                i['from'], i['to'],
                i['give'], i['from'], i['get'], i['to'],
                i['link'],
                i['to'], i['sell'],
                i['spread_abs'], i['spread_proc']
            ))

    await message.answer(text)


@dp.message_handler(Text(equals="Настройки⚙️"), state=StatesChange.STATE_EMPTY)
async def parameters_get1(message: types.Message):
    await parameters_get(message)


@dp.message_handler(Text(equals="Обновить🔃"), state=StatesChange.STATE_EMPTY)
async def update_get1(message: types.Message):
    await update_get(message)


@dp.message_handler(state=StatesChange.STATE_VALUE)
async def process_value_change(message: types.Message):
    parameters["value"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_SPREAD)
async def process_value_change(message: types.Message):
    parameters["min_spread"] = float(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_MIN_GOOD)
async def process_value_change(message: types.Message):
    parameters["min_good"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_MAX_BAD)
async def process_value_change(message: types.Message):
    parameters["max_bad"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_EMPTY)
async def echo(message: types.Message):
    await message.answer("Не знаю такой команды =(")


if __name__ == '__main__':
    start_listening()
    main()
