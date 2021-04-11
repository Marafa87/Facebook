from pymongo import MongoClient

# @app.route('/ro')
def displayAllDb():

    client = MongoClient("mongodb+srv://ali:Mygema2022@cluster0.kzhhb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["Titanic_Dataset"]
    df = list(db.Mini_Titanic.distinct("Age"))
    # dt = client.list_database_names()
    return df
    # "Haladou Issa Ali"
 