from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.db import db_videos_get_all
from keyboards.inline.callback_datas import start_quest_callback, main_menu_callback, return_to_menu_callback


def start_quest():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="ПОЛУЧИТЬ БОНУСЫ!", callback_data=start_quest_callback.new())
                ]
            ],
        )


def return_to_menu():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data=return_to_menu_callback.new())
                ]
            ],
        )


def main_menu():
    videos = db_videos_get_all()
    videos_id = [int(i['_id']) for i in videos]
    keyboard = [InlineKeyboardButton(text=f"{i}", callback_data=main_menu_callback.new(name=f"{i}")) for i in sorted(videos_id)]
    return InlineKeyboardMarkup(row_width=5).add(*keyboard)
