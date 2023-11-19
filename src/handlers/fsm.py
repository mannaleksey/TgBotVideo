from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from config.config import cfg_to_change, cfg
from keyboards.reply.keyboard_markup import main_reply_keyboard
from loader import dp, bot
from aiogram.utils.markdown import escape_md

teh_chat_id = cfg['dev_chat_id']
message_seneded = cfg_to_change['message_seneded']


class FSMQuestion(StatesGroup):
    text = State()


async def new_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await state.finish()
    if message.text == 'Отмена':
        await message.answer(text='Действие отменено', reply_markup=main_reply_keyboard())
        return
    if message.chat.username is None:
        who = "Ник не установлен"
    else:
        who = "@"+message.chat.username
    await message.reply(f"{message_seneded}",
                        parse_mode='Markdown', reply_markup=main_reply_keyboard())
    await bot.send_message(teh_chat_id,
                           f"✉  Новый вопрос\nОт: {escape_md(who)}\nВопрос: `{data['text']}`\n\n📝 Чтобы ответить на вопрос введите `/ответ {message.chat.id} Ваш ответ`",
                           parse_mode=ParseMode.MARKDOWN)


def register_handler_fsm():
    dp.register_message_handler(new_question, state=FSMQuestion.text, content_types=['photo', 'text'])
