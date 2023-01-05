import pymongo
from pymongo.errors import BulkWriteError

class MongoDB:
    def __init__(self, dbName, colName, MONGO_URL):
        self.dbName = dbName
        self.colName = colName
        self.MONGO_URL = MONGO_URL

    def connectDB(self):
        """
        make connection to database and collection
        :return: collection
        """
        dbName = self.dbName
        colName = self.colName
        dbConn = pymongo.MongoClient(self.MONGO_URL, tlsAllowInvalidCertificates = True)
        db = dbConn[dbName]
        collection = db[colName]
        return collection

class NewsDB(MongoDB):
    def __init__(self, dbName, colName, MONGO_URL):
        super(NewsDB, self).__init__(dbName, colName, MONGO_URL)

    def findAllNews(self, collection):
        """
        Get all the news from collection
        :return: iterator of dictionary
        """
        try:
            allNews = collection.find({})
        except:
            allNews = []

        return allNews

    def findTop20News(self, collection):
        """
        Get 20 recent news from collection, descending order
        :return: iterator of dictionary
        """
        try:
            allNews = collection.find({}).sort("created_at", -1).limit(20)
        except:
            allNews = []

        return allNews

    def insertOneNews(self, collection, dict1):
        """
         Given a json(news record), insert it into news collection
        """
        try:
            collection.insert_one(dict1)
            print("Success: insert one new")
        except Exception as e:
            print(e)


    def insertManyNews(self, collection, lst):
        """
         Given a list of json(news record), insert all of them into news collection
        """
        try:
            collection.insert_many(lst, ordered = False)
            print("Success: insert a batch of news")
        except BulkWriteError as e:
            print("You have submitted duplicate news, and all other news are successfully submitted.")
            print(str(e))
        except Exception as e:
            print("Some error happened, and all other news are successfully submitted.")
            print(e)

    def getNewsCount(self, collection):
        raise NotImplementedError



