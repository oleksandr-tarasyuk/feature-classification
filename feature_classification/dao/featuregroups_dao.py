from bson import ObjectId


class FeatureGroupDao:

    def __init__(self, goldenspear_db, collection_name):
        self.collection = goldenspear_db[collection_name]

    def get_element(self, id: str) -> dict:
        """
        This method gets and returns the element in the sp db given the product id.
        :param id: target product id
        :return: product entry
        """
        return self.collection.find_one({'_id': ObjectId(id)})

    def get_feature_groups(self) -> list:
        """
        This method gets all the products that are not published containing an specific product category

        Returns:
            list: products with the same product category
        """
        query = {}
        projection = {"name": 1, "appName": 1, "genome": 1, "children": 1}
        out = {}
        for result in self.collection.find(query, projection):
            out[result["_id"]] = result
        return out
