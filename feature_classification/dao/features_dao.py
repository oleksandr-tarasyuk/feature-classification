from bson import ObjectId


class FeatureDao:

    def __init__(self, goldenspear_db, collection_name):
        self.collection = goldenspear_db[collection_name]

    def get_element(self, id: str) -> dict:
        """
        This method gets and returns the element in the sp db given the product id.
        :param id: target product id
        :return: product entry
        """
        return self.collection.find_one({'_id': ObjectId(id)})

    def get_features(self) -> list:
        """
        This method gets all the products that are not published containing an specific product category
        Args:
            input_id (str): id of the product category to be retrieved
        Returns:
            list: products with the same product category
        """
        query = {}
        projection = {"name": 1, "genome": 1, "genomeView": 1, "featureGroup": 1}
        return list(self.collection.find(query, projection))

    def get_features_by_group(self, feature_group_id: str) -> list:
        """
        This method gets all the products that are not published containing an specific product category
        Args:
            input_id (str): id of the product category to be retrieved
        Returns:
            list: products with the same product category
        """
        query = {"featureGroup": ObjectId(feature_group_id)}
        projection = {"name": 1, "genome": 1, "genomeView": 1}
        return list(self.collection.find(query, projection))
