from pymongo import MongoClient
import numpy as np

def GetDB():
    cluster = MongoClient(f'mongodb+srv://ajm1102:{os.environ.get("ajm1102")}@cluster0.ruv0x.mongodb.net'
                          f'/myFirstDatabase?retryWrites '
                          '=true&w=majority')
    db = cluster["Infection_Simulations"]
    return db


