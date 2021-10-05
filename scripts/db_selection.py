import os
import random
import pickle
import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId

from interest import feature_groups_of_interest, pc_of_interest, origins_yes
from config import mongo_url

MIN_FOR_PC = 200
MIN_FOR_FEAT = 40


class DBSelector:
    def __init__(self, accept_file, discard_file, save_products=False, pkl_path=None):
        self.product_collection = None
        self.feature_collection = None
        self.pc_collection = None
        self.products = []
        self.priority_products = []
        self.accepted = []
        self.discarded = []
        self.groups = []
        self.features_from_groups = []
        self.features_from_groups_dict = {}
        self.accept_file = accept_file
        self.discard_file = discard_file
        self.save_products = save_products
        self.pkl_path = pkl_path
        self.get_collections()
        self.load_products()

    def get_collections(self):
        db_connection = pymongo.MongoClient(mongo_url)
        db = db_connection['goldenspear']

        self.product_collection = db['product']
        self.feature_collection = db['feature']
        self.pc_collection = db['productcategory']

    def load_groups(self):
        self.groups = [ObjectId(grp) for grp in feature_groups_of_interest]

    def load_features(self):
        features_from_groups_tuple = \
            [(feat['_id'], feat['name'])
             for feat in list(self.feature_collection.find({"featureGroup": {'$in': self.groups}}))]
        self.features_from_groups = [ft[0] for ft in features_from_groups_tuple]
        for ft in features_from_groups_tuple:
            self.features_from_groups_dict[ft[0]] = ft[1]

    def load_products(self):
        self.load_groups()
        self.load_features()
        if self.check_if_pkl():
            self.load_products_from_pkl()
        else:
            self.load_products_from_db()
            self.load_features_of_products()
            self.order_products()
            if self.save_products:
                self.save_pkl()

    def check_if_pkl(self):
        return os.path.exists(self.pkl_path)

    def load_products_from_pkl(self):
        with open(self.pkl_path, 'rb') as f:
            self.products = pickle.load(f)

    def save_pkl(self):
        with open(self.pkl_path, 'wb') as f:
            pickle.dump(self.products, f)

    def load_products_from_db(self):
        projection = {"_id": 1,
                      "productDescription.features.featId": 1,
                      "productDescription.categories": 1,
                      "prevImage.url": 1}
        self.products = list(self.product_collection.find({"config.origin": {'$in': origins_yes}}, projection))

    def load_features_of_products(self):
        self.features_of_product = {}
        for prod in self.products:
            self.features_of_product[prod['_id']] = \
                [feature['featId'] for feature in prod['productDescription']['features']]

    def clear_priority_products(self):
        self.priority_products = []

    def order_products(self):

        self.clear_priority_products()

        random.shuffle(self.products)

        cat_id_to_name = {}
        for pc in self.pc_collection.find({}, {"_id": 1, "name": 1}):
            cat_id_to_name[pc['_id']] = pc['name']

        for pc in pc_of_interest:
            while True:
                try:
                    products_of_pc = [prod for prod in self.products
                                      if pc in [cat_id_to_name[cat]
                                                for cat in prod['productDescription']['categories']]][:MIN_FOR_PC]
                    break
                except KeyError as cat_error:
                    cat_id_to_name[ObjectId(str(cat_error).replace("ObjectId('", "").replace("')", ""))] = 'NOCAT'
            self.priority_products += products_of_pc

        for ft in self.features_from_groups:
            print(self.features_from_groups_dict[ft])
            products_of_ft = \
                [prod for prod in self.products if ft in self.features_of_product[prod['_id']]][:MIN_FOR_FEAT]
            self.priority_products += products_of_ft

        self.priority_products = json.loads(json_util.dumps(self.priority_products))

        for iprod in range(len(self.priority_products)):
            self.priority_products[iprod]['_id'] = ObjectId(self.priority_products[iprod]['_id']['oid'])
            for ifeat in range(len(self.priority_products[iprod]['productDescription']['features'])):
                self.priority_products[iprod]['productDescription']['features'][ifeat]['featId'] = \
                    ObjectId(self.priority_products[iprod]['productDescription']['features'][ifeat]['featId']['oid'])
            for icat in range(len(self.priority_products[iprod]['productDescription']['categories'])):
                self.priority_products[iprod]['productDescription']['categories'][icat] = \
                    ObjectId(self.priority_products[iprod]['productDescription']['categories'][icat]['oid'])

        no_priority_products = [sel for sel in self.products if sel not in self.priority_products]

        self.products = self.priority_products + no_priority_products

    def product_retriever(self):
        for product in self.products:
            yield product

    def get_product_length(self):
        return len(self.products)

    @staticmethod
    def save_product(text_file, product):
        with open(text_file, 'w+') as f:
            f.write(product['_id'])

    def accept_product(self, product):
        self.accepted.append(product)
        self.save_product(self.accept_file, product)
        return self.get_num_accepted_products()

    def discard_product(self):
        self.discarded.append(product)
        self.save_product(self.discard_file, product)

    def get_num_accepted_products(self):
        return len(self.accepted)

    def feat_name_from_id(self, feat_id):
        if feat_id in self.features_from_groups_dict:
            return self.features_from_groups_dict[feat_id] \
                if self.features_from_groups_dict[feat_id] is not None else 'NONE'
        else:
            return 'UNKNOWN'


if __name__ == "__main__":
    ACCEPT_FILE = '/home/imas/accepted.txt'
    DISCARD_FILE = '/home/imas/discarded.txt'
    PKL_PATH = '/home/imas/products.pkl'
    db_selector = DBSelector(ACCEPT_FILE, DISCARD_FILE, save_products=True, pkl_path=PKL_PATH)
    retriever = db_selector.product_retriever()
    while(True):
        retrieved_product = next(retriever)
        print(product)
