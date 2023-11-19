import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEV_CHAT = os.getenv("DEV_CHAT")
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB
cfg_mongo = {
    'db_name': 'tg',
    'collection_profiles': 'profiles',
    'collection_videos': 'videos',
}

# To Change
cfg_to_change = {
    'welcome_message': 'Приветствую тебя!',
    'sub_msg': 'За подпиской обращаться к @return_python',
    'message_seneded': '✉ Ваш вопрос был отослан! Ожидайте ответа от тех.поддержки.',
    'question_type_ur_question_message': '📝 Введите ваш вопрос:',
    'error_message': 'Упс! *Ошибка!* Не переживайте, ошибка уже *отправлена* разработчику.',
}

# Admin
ERROR_CHAT = os.getenv("ERROR_CHAT")
cfg = {
    'dev_chat_id': DEV_CHAT,
    'error_chat_id': ERROR_CHAT,
    'sub': 'Пользователь с подпиской',
    '1lvl_adm_name': 'Тех.поддержка',
    '2lvl_adm_name': 'Администратор',
    '3lvl_adm_name': 'Руководитель'
}
