from pymongo import MongoClient
from config.config import MONGODB_URL, cfg_mongo

db = cfg_mongo['db_name']

client = MongoClient(MONGODB_URL)
db = client[db]
profiles = db[cfg_mongo['collection_profiles']]
videos = db[cfg_mongo['collection_videos']]


def db_profile_exist(uid):
    if profiles.find_one({"_id": uid}):
        return True
    else:
        return False


def db_profile_exist_usr(username):
    if profiles.find_one({"username": username}):
        return True
    else:
        return False


def db_profile_insert_one(query):
    return profiles.insert_one(query)


def db_profile_access(uid):
    return profiles.find_one({'_id': uid})['access']


def db_profile_banned(uid):
    if profiles.find_one({'_id': uid})['ban'] == 1:
        return True
    else:
        return False


def db_profile_update_one(query, query2):
    return profiles.update_one(query, query2)


def db_profile_get_username(username, get):
    return profiles.find_one({'username': username})[get]


def db_videos_get_all():
    return [i for i in videos.find()]


def db_get_video_from_id(_id):
    return videos.find_one({'$or': [{"_id": str(_id)}, {"_id": int(_id)}]})
