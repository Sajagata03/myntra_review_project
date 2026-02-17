# this whole file is for mongodb connection

import pandas as pd
from database_connect import mongo_operation as mongo 
import os, sys
from src.constants import *
from src.exception import CustomException


# this class is made to interact with mongodb database for storing and retrieving product reviews
class MongoIO:
    mongo_ins = None   # a level variable to establish the connection for only once during the lifetime of the application

    def __init__(self):
        if MongoIO.mongo_ins is None:
            mongo_db_url = "mongodb+srv://sajagataojha_db_user:vminkook2003@cluster0.c3nxqj9.mongodb.net/?appName=Cluster0"
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
            MongoIO.mongo_ins = mongo(client_url=mongo_db_url,
                                      database_name=MONGO_DATABASE_NAME)
        self.mongo_ins = MongoIO.mongo_ins

# in the below function (method) we are storing reviews
    def store_reviews(self,
                      product_name: str, reviews: pd.DataFrame):
        try:
            collection_name = product_name.replace(" ", "_")
            self.mongo_ins.bulk_insert(reviews,
                                       collection_name)

        except Exception as e:
            raise CustomException(e, sys)

# in the below function we are getting the review from mongo db
    def get_reviews(self,
                    product_name: str):
        try:
            data = self.mongo_ins.find(
                collection_name=product_name.replace(" ", "_")
            )

            return data

        except Exception as e:
            raise CustomException(e, sys)


