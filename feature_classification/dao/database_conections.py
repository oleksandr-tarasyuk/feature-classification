import os

import pymongo

from feature_classification.dao.featuregroups_dao import FeatureGroupDao
from feature_classification.dao.features_dao import FeatureDao
from feature_classification.dao.products_dao import ProductDao


def __get_mongo_client():
    usr = os.environ.get('MONGO_USR', 'newroot')
    pwd = os.environ.get('MONGO_PWD', 'WT8tP3ME3cYvlmUP')
    url = os.environ.get('MONGO_URL', '209.133.201.254/?authSource=admin')

    print(f"Connecting to database: {url}")
    mongo_url = f"mongodb://{usr}:{pwd}@{url}"

    return pymongo.MongoClient(mongo_url)


def __get_ces_db(db: str):
    return __get_mongo_client()[db]


def get_product_dao():
    mongo_db = __get_ces_db('goldenspear')
    return ProductDao(mongo_db, "product")


def get_feature_dao():
    mongo_db = __get_ces_db('goldenspear')
    return FeatureDao(mongo_db, "feature")


def get_feature_group_dao():
    mongo_db = __get_ces_db('goldenspear')
    return FeatureGroupDao(mongo_db, "featuregroup")
