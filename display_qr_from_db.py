from io import BytesIO
from pymongo import MongoClient
from PIL import Image, ImageTk
import json
DB_PASSWORD = ''

with open("private.json") as private_config:
    private = json.loads(private_config.read())
    DB_PASSWORD = private['password']

client = MongoClient(
    f"mongodb+srv://test:{DB_PASSWORD}@cluster0-pncd0.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('pilot')
users = db.users
for u in users.find():
    im = Image.open(BytesIO(u['img']))
    im.show()
