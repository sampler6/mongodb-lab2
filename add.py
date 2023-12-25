import json
from db import shop

#with open("shop.json", "r", encoding="UTF-8") as f:
    #d = json.load(f)
    #for i in d:
        #shop.insert_one(i)

for i in shop.find():
    print(i)


