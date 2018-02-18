import pymongo
import sys
try:
    import secret_stuff
except ModuleNotFoundError:
    print("Please create secret_stuff.py, go to github "
          "https://github.com/Grewoss/duckman-python_bot/blob/master/secret_stuff.py "
          "to see an example.")
    sys.exit(0)

client = pymongo.MongoClient(secret_stuff.database_token())

discord_db = client.discord_db

user_base = discord_db.users


class DataBase:

    async def create_user(self, user_id: int, user_name):
        try:
            post = {
                "_id": user_id,
                "user_name": user_name,
                "levels": 0,
                "xp": 0,
                "gamble_won": 0,
                "gamble_lost": 0
            }
            post_id = user_base.insert_one(post).inserted_id
            return post_id
        except:
            return None

    async def find_user(self, user_id: int):
        try:
            found = list(user_base.find({"_id": user_id}))[0]
            return found
        except Exception as e:
            print(e)
            return None

    async def update_user(self, user_id: int, change_dict: dict):
        try:
            update = user_base.update_one({
                "_id": user_id}, {
                    "$set": change_dict
                })
            return update
        except Exception as e:
            print(e)
            return None

    async def get_all(self):
        try:
            data = user_base.find()
            r_data = {}
            for d in data:
                r_data[d["_id"]] = d
            return r_data
        except Exception as e:
            print(e)
            return None

    # def deleted_user_base(self):
    #     result = user_base.delete_many({})
    #     return result


if __name__ == "__main__":
    print("DataBase started")
    db = DataBase().get_all()
    print(db)
else:
    print("Database import success")
