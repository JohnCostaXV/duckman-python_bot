import pymongo
import secret_stuff

print("DataBase started")

client = pymongo.MongoClient(secret_stuff.database_token())

discord_db = client.discord_db

user_base = discord_db.users


class DataBase:

    def create_user(self, user_id: int, user_name):
        try:
            post = {
                "_id": user_id,
                "user_name": user_name,
                "levels": [],
                "xp": 0
            }
            post_id = user_base.insert_one(post).inserted_id
            return post_id
        except:
            return None

    def find_user(self, user_id: int):
        try:
            found = list(user_base.find({"_id": user_id}))[0]
            return found
        except Exception as e:
            print(e)
            return None

    def update_user(self, user_id: int, change_dict: dict):
        update = user_base.update_one({
            "_id": user_id}, {
                "$set": change_dict
            })
        return update

    def deleted_user_base(self):
        result = user_base.delete_many({})
        return result