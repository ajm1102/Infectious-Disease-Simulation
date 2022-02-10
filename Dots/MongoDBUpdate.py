from pymongo import MongoClient
import os
from statistics import mean


def GetDB():
    cluster = MongoClient(f'mongodb+srv://ajm1102:{os.environ.get("ajm1102")}@cluster0.ruv0x.mongodb.net'
                          f'/myFirstDatabase?retryWrites '
                          '=true&w=majority')
    db = cluster["Infection_Simulations"]
    return db


def CalAvgAndUpload(db):
    # Possibly use update many
    for record in db.Simulations.find():
        avg_numpeople_left_inf = mean(record["results"][-1]["Infected"])
        percent_Infected = round((avg_numpeople_left_inf/record["Number_people"]) * 100, 1)
        db.Simulations.update_one({"_id": record["_id"]}, {"$set": {"Percent_left_infected": percent_Infected}})
    return


def main():
    db = GetDB()
    CalAvgAndUpload(db)
    return


if __name__ == "__main__":
    main()
