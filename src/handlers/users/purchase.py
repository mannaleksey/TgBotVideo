from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaVideo

from handlers.fsm import FSMQuestion

from config.config import cfg, cfg_to_change
from handlers.db import db_profile_insert_one, db_profile_exist, db_profile_banned, db_get_video_from_id, \
    db_profile_access
from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.choice_buttons import main_menu
from keyboards.reply.keyboard_markup import *
from loader import dp, bot

welcome_message = cfg_to_change['welcome_message']

sub_msg = cfg_to_change['sub_msg']
question_first_msg = cfg_to_change['question_type_ur_question_message']


errormessage = cfg_to_change['error_message']
error_chat_id = cfg['error_chat_id']


async def subscription(message: Message):
    await message.answer(text=sub_msg)


async def course(message: Message):
    uid = message.from_user.id
    if db_profile_access(uid) >= 0:
        video_data = db_get_video_from_id(1)
        await message.answer_video(
            video=video_data['file_id'],
            caption=f"Видео №{video_data['_id']}\n{video_data['description']}",
            reply_markup=main_menu()
        )
    else:
        await message.answer(text=f'Просмотр курсов доступен только по подписке\n{sub_msg}')


async def show_course(call: CallbackQuery, callback_data: dict):
    uid = call.from_user.id
    if db_profile_access(uid) >= 0:
        videos = db_videos_get_all()
        videos_id = [int(i['_id']) for i in videos]
        if int(callback_data["name"]) in videos_id:
            video_data = db_get_video_from_id(int(callback_data["name"]))
            await call.message.edit_media(
                media=InputMediaVideo(
                    media=video_data['file_id'],
                    caption=f"Видео №{video_data['_id']}\n{video_data['description']}"
                ),
                reply_markup=main_menu()
        )
    else:
        await call.answer(text=f'Просмотр курсов доступен только по подписке\n{sub_msg}')


async def cancel_to_menu(message: Message):
    await message.answer(text='Действие отменено', reply_markup=main_reply_keyboard())


async def feedback(message: Message):
    try:
        if db_profile_banned(message.from_user.id):
            await message.answer("⚠ Вы *заблокированы* у бота!", parse_mode='Markdown')
            return
        await message.answer(f"{question_first_msg}", reply_markup=return_to_menu())
        await FSMQuestion.text.set()

    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}", parse_mode='Markdown')
        await bot.send_message(error_chat_id, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')


async def start_program(message: Message):
    try:
        if message.chat.type != 'private':
            await message.answer('Данную команду можно использовать только в личных сообщениях с ботом.')
            return
        if db_profile_exist(message.from_user.id):
            await message.answer(f'{welcome_message}', parse_mode='Markdown', reply_markup=main_reply_keyboard())
        else:
            db_profile_insert_one({
                '_id': message.from_user.id,
                'username': message.from_user.username,
                'access': -1,
                'ban': 0
            })
            print('Новый пользователь!')
            await message.answer(f'{welcome_message}', parse_mode='Markdown', reply_markup=main_reply_keyboard())
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(error_chat_id, f"Случилась *ошибка* в чате *{cid}* в функции start program\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')


async def get_id(message: Message):
    if message.chat.type != 'private':
        await message.answer(f'Group_id: {message.chat.id}')
        return


async def answer(message: Message):
    if message.video:
        if db_profile_access(message.from_user.id) >= 3:
            await message.reply(text=f"{message.video.file_id}")
    if message.chat.type != 'private':
        return
    await message.reply('Я тебя не понимаю.')
    await message.answer_video('BAACAgIAAxkBAAM8ZVfE-WeWsHCHFooSGoifZzaEanYAAv80AAJPmMBK9cp5CbUuPXgzBA')
    await message.answer_video('BAACAgIAAxkBAAIDHmVaFFp_gyjcBJVVJXp9v7QlaBW3AALfNQACKDPRSq502_h-6OZPMwQ')


def register_handler_client():
    dp.register_message_handler(subscription, text='Подписка')
    dp.register_message_handler(course, text='Курс')
    dp.register_message_handler(cancel_to_menu, text='Отмена')
    dp.register_message_handler(feedback, text='Обратная связь')
    dp.register_message_handler(start_program, Command("start"))
    dp.register_message_handler(get_id, Command("get_id"))
    dp.register_message_handler(answer, content_types=types.ContentType.ANY)

    dp.register_callback_query_handler(show_course, main_menu_callback.filter())
