import json
import re

import pandas as pd
from loguru import logger
from pandas.core.frame import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

json_path = "products.json"
stopwords = list(fr_stop) + list(en_stop)


def prepare_dataframe_from_json():
    logger.info("Preparing Dataframe from JSON")
    with open(json_path) as json_file:
        data = json.load(json_file)

    product_list = data["data"]
    ID, categorie_produit, description_produit, nom_produit, tags_produit = ([] for _ in range(5))
    for product in product_list:
        ID.append(product["_id"])
        nom_produit.append(product["nom_produit"])

        try:
            categorie_produit.append(product["categorie_produit"])
        except:
            categorie_produit.append("UN")

        try:
            tags_produit.append(product["tags_produit"])
        except:
            tags_produit.append(None)

        try:
            description_produit.append(product["description_produit"])
        except:
            description_produit.append("")

        len(description_produit)
    return pd.DataFrame(
        {'id': ID,
         'nom_produit': nom_produit,
         'categorie_produit': categorie_produit,
         'tags_produit': tags_produit,
         'description_produit': description_produit
         })


def merge_remove_duplicate(tags_list: list, description: str):
    tags = ' '.join(tags_list)
    tags = tags + ' ' + description
    tags = re.sub(r'[^\w\s]', '', tags)
    tags = ' '.join(set(tags.lower().split()))
    return tags


def create_text_column_and_indices(df: DataFrame):
    logger.info("Creating indices")
    final_text = []
    for index, row in df.iterrows():
        final_text.append(merge_remove_duplicate(row['tags_produit'], row['description_produit']))
    df["text"] = final_text
    indices = pd.Series(df.index, index=df['id'])
    return df, indices


def create_similarity_matrix(df: DataFrame):
    logger.info("Create Similarity Matrix")
    tfidf_vectorizer = TfidfVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2))
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["text"])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_recommendations(product_id, indices, dataframe, cosine_sim):
    logger.info("Calculating recommendations")
    idx = indices[product_id]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    products_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return dataframe['id'].iloc[products_indices]


def response_envelop(rec):
    recommendations = {}
    for i in range(len(rec.values)):
        recommendations[i + 1] = rec.values[i]
    return recommendations
