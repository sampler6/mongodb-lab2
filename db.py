import pymongo

client = pymongo.MongoClient('192.168.112.103')
database = client['22304']
shop = database['korzhuk-shop']