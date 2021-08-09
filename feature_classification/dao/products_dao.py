from bson import ObjectId


class ProductDao:

    def __init__(self, goldenspear_db, collection_name):
        self.collection = goldenspear_db[collection_name]

    def get_products_from_sp(self):
        query = {"config.origin": 'shoepalace_test_new_genome'}
        projection = {"title": 1, "gender": 1, "productDescription": 1, "contents": 1}
        products = list(self.collection.find(query, projection))
        return list(zip(products, ['sp'] * len(products)))

    def get_element(self, id: str) -> dict:
        """
        This method gets and returns the element in the sp db given the product id.
        :param id: target product id
        :return: product entry
        """
        return self.collection.find_one({'_id': ObjectId(id)})

    def get_whole_products_published(self, limit_low: int, limit_top: int) -> list:
        """
        This method gets all the products that are published containing an specific product category
        Args:
            limit_top (int): upper limit in order to get the maximum segment of the query
            limit_low (int): lower limit in order to get the minimum segment of the query
        Returns:
            list: products with filtered by limits
        """
        query = {"config.published": True, "config.origin": {
            "$nin": ["sp_test_new_genome_new_types", "shoepalace_test_new_genome", "sp_test_new_genome_nottagged"]}}
        projection = {"name": 1, "gender": 1, "information": 1, "productDescription": 1, "config.origin": 1,
                      "contents": 1}
        out = []
        counter = 0
        limit_top = limit_top - limit_low
        for item in self.collection.find(query, projection).skip(limit_low).limit(limit_top):
            counter += 1
            if counter % 1000 == 0:
                print(counter)
            out.append(item)
        return out

    def get_product_by_cat(self, input_id: str) -> list:
        """
        This method gets all the products that are not published containing an specific product category
        Args:
            input_id (str): id of the product category to be retrieved
        Returns:
            list: products with the same product category
        """
        query = {"config.published": False, "config.origin": {
            "$nin": ["sp_test_new_genome_new_types", "shoepalace_test_new_genome", "sp_test_new_genome_nottagged"]},
                 "productDescription.categories": ObjectId(input_id)}
        projection = {"name": 1, "gender": 1, "productDescription.categories": 1, "config.origin": 1,
                      "contents": 1}
        return list(self.collection.find(query, projection))
