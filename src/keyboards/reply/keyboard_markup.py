from aiogram.types import ReplyKeyboardMarkup

from handlers.db import db_videos_get_all


def main_reply_keyboard():
    main = ReplyKeyboardMarkup(resize_keyboard=True)
    main.add('Подписка').add('Курс').add('Обратная связь')
    return main


def course_reply_keyboard_and_desc():
    videos = db_videos_get_all()
    course = ReplyKeyboardMarkup(resize_keyboard=True)
    # for _id in videos_id:
    #     course.add(_id)
    course.add('Вернуться назад')
    course.add(*[i['_id'] for i in videos])
    return course, videos


def return_to_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add("Отмена")
