import pickle

from nltk import FreqDist
import nltk
from feature_classification.dao.database_conections import get_product_dao, get_feature_dao, get_feature_group_dao
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
import numpy as np

nltk.download('punkt')


def analyze_sentiment(text):
    tokenized_word = tokenizer.tokenize(text)
    stemmed_words = []
    for w in tokenized_word:
        if w not in stop_words:
            stemmed_words.append(stem.stem(w))
    return stemmed_words


def analyze_data(feature_coun, counter):
    for feat_id, feat_texts in feature_coun.items():
        fdist = FreqDist(feat_texts["text"])
        plt.title(feat_id)
        fdist.plot(30, cumulative=False)
        plt.savefig(f'resources/images_{str(counter)}/{feat_id}.png')


def merge_by_fg(features_scope):
    dict_group = {}
    for key_fet, value_fet in features_scope.items():
        try:
            if value_fet["group_name"] in dict_group:
                dict_group[value_fet["group_name"]] = {
                    "text": dict_group[value_fet["group_name"]]["text"] + value_fet["text"],
                    "count": value_fet["count"] + dict_group[value_fet["group_name"]]["count"]}
            else:
                dict_group[value_fet["group_name"]] = {"text": value_fet["text"], "count": value_fet["count"]}
        except Exception as err:
            print(f"some errors in merging features as {err}")
    return dict_group


def load_db(limit_low, limit_top):
    path_products = f"resources/products_254_{limit_low}_{limit_top}.pkl"
    try:
        with open(path_products, "rb") as input_file:
            product_saas = pickle.load(input_file)
        print("Loaded products")
    except FileNotFoundError:
        product_saas = db_products.get_whole_products_published(limit_low, limit_top)
        with open(path_products, 'wb') as handle:
            pickle.dump(product_saas, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Read 254 products")
    return product_saas


def plot_bar(feat_plot, i):
    plt.figure(figsize=(8, 15))
    height = feat_plot.values()
    bars = feat_plot.keys()
    y_pos = np.arange(len(bars))
    # Create horizontal bars
    plt.barh(y_pos, height)

    # Create names on the x-axis
    plt.yticks(y_pos, bars)
    plt.savefig(f'resources/images_{str(i)}/0barplot.png')


def main():  # noqa: C901
    for total_counter in range(2, 4):
        products = []
        counter = total_counter + 1
        total_counter *= 4

        for i in range(total_counter, total_counter + 4):
            low = i * 50000
            high = low + 49999
            print(f"{low} and {high}")
            products += load_db(low, high)

        features = db_features.get_features()
        feature_groups = db_feature_groups.get_feature_groups()

        feature_count = {}
        for feature in features:
            try:
                feature_count[str(feature["_id"])] = {
                    "text": [], "count": 0, "feat_name": feature['name'],
                    "group_name": feature_groups[feature["featureGroup"]]['name']}
            except KeyError as e:
                print(f"key {e} not found")

        for i, product in enumerate(products):
            try:
                text_steamed = analyze_sentiment(product["information"])
                print(i)
                for feature_product in product["productDescription"]['features']:
                    try:
                        feature_count[str(feature_product['featId'])]["text"].extend(text_steamed)
                        feature_count[str(feature_product['featId'])]["count"] += 1
                    except KeyError as e:
                        pass
                        print(f"key {e} not found")
            except KeyError as e:
                print(f"key {e} not found")
                pass

        feature_group_count = merge_by_fg(feature_count)
        feat_plot = {}
        for key, val in feature_group_count.items():
            feat_plot[key] = val['count']
        plot_bar(feat_plot, counter)
        analyze_data(feature_group_count, counter)


if __name__ == '__main__':
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    db_features = get_feature_dao()
    db_products = get_product_dao()
    db_feature_groups = get_feature_group_dao()
    stem = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    main()
