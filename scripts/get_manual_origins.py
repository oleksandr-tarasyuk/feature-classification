import os
import random
import pymongo
import matplotlib.pyplot as plt
from PIL import Image
from bson.objectid import ObjectId

from interest import feature_groups_of_interest, pc_of_interest
from config import mongo_url


class FeatDictHandler:

    def __init__(self, featdict):
        self.feat_dict = featdict

    def feat_id_to_name(self, id):
        return self.feat_dict[id]


def plot_prod_info(collection, origin, feat_handler, init=0):
    """
    For a given origin, this generator iterates all its products by showing the info (origin and features

    :param collection: (pymongo.collection.Collection) products full collection to query
    :param origin: (str) origin name to iterate
    :param feat_handler: (FeatDictHandler) object, used to get feature names from id
    :param init: (int) position in which to start, used to skip the desired positions
    :return:
    """
    needed_projection = {'contents.url': 1,
                         "productDescription.features.featId": 1,
                         "productDescription.features.partId": 1}
    products_from_origin = collection.find({"config.origin": origin}, needed_projection)
    for ii, product in enumerate(products_from_origin):
        if ii < init:
            continue
        print('Origin:' + origin)
        for feat in product['productDescription']['features']:
            print(feat_handler.feat_id_to_name(feat['featId']))
        img = Image.open('/fileserver1/webdata/' + product['contents'][0]['url'])
        plt.imshow(img)
        yield ''


if __name__ == "__main__":
    """
    This script is used to review the origins for the products in e-Commerce db and select the wanted origins. At the 
    end they are printed, so they can be added to interests.py as origins_yes. Requires to have in interests.py the 
    variables feature_groups_of_interest (list of strings of the ids of the desired feature groups) and pc_of_interest 
    (list of strings of the desired pcs)  
    """
    db_connection = pymongo.MongoClient(mongo_url)
    db = db_connection['goldenspear']


    collection = db['product']
    feature_collection = db['feature']

    groups = [ObjectId(grp) for grp in feature_groups_of_interest]
    features_from_groups = [feat['_id'] for feat in list(feature_collection.find({"featureGroup": {'$in': groups}}))]

    fgroups_query = {"productDescription.features.featId": {'$in': features_from_groups}}
    origin_projection = {'config.origin': 1}
    products_from_fgroups = list(collection.find(fgroups_query, origin_projection))
    product_origins_from_fgroup_nonproc = [produ['config']['origin'] for produ in products_from_fgroups]

    product_origins_from_fgroup = []
    for origin in product_origins_from_fgroup_nonproc:
        if isinstance(origin, list):
            for single_origin in origin:
                product_origins_from_fgroup.append(single_origin)
        else:
            product_origins_from_fgroup.append(origin)
    product_origins_from_fgroup_unique = list(set(product_origins_from_fgroup))

    for origin in product_origins_from_fgroup_unique:
        num_published = collection.find({"config.origin": origin}, {}).count()
        print(origin + ': ' + str(num_published))

    feat_dict = {}
    for feat in feature_collection.find({}, {"_id": 1, "name": 1}):
        feat_dict[feat['_id']] = feat['name']
    feathand = FeatDictHandler(featdict)

    groups_yes = []
    groups_no = []
    while True:
        print('Write origin to view: (Q to Quit)')
        origin = input()
        if origin == 'Q':
            break
        plot_gen = plot_prod_info(collection, origin, feathand, 0)
        while True:
            try:
                next(plot_gen)
                print('Write "N" to next, other to another origin:')
                option = input()
                if option != 'N':
                    print('Save origin? (Y/N)')
                    save = input()
                    if save == 'Y':
                        groups_yes.append(origin)
                    elif save == 'N':
                        groups_no.append(origin)
                    break
            except Exception as e:
                print(e)
                break

    print(groups_yes)

    products_from_good_origins = collection.find({"config.origin": {'$in': groups_yes}}, {})
    num_products = products_from_good_origins.count()

    print('SELECTED: ')
    print(groups_yes)
    print('DISCARDED: ')
    print(groups_yes)

    print('Write these origins to interest.py "origins_yes" before running order_products method of db_selection.py')
