from io import BytesIO
from pymongo import MongoClient
from PIL import Image, ImageTk

client = MongoClient('localhost', 27017)
db = client.get_database('pilot')
users = db.users
for u in users.find():
    im = Image.open(BytesIO(u['img']))
    im.show()
