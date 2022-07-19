import sys
import os

sys.path.append(os.path.dirname(__file__))

from ner import entities
import allennlp
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
from allennlp_models.pretrained import load_predictor
predictor = load_predictor("structured-prediction-srl-bert")
import pickle
from nltk.tokenize import word_tokenize
import re
from sklearn.cluster import linkage_tree
import spacy
from lemminflect import getInflection, getAllInflections

import nltk

dirname = os.path.dirname(__file__)

nltk.download("punkt")

nlp = spacy.load("en_core_web_sm")

with open(os.path.join(dirname, "products.pickle"), "rb") as target:
    products = pickle.load(target)

with open(os.path.join(dirname, "keyword_list.pickle"), "rb") as target:
    keyword_list = pickle.load(target)

def is_topic_of_interest(text):
    """returns true if lemma of interest appears in headline and number of
    entities with label 'ORG' is at least 2

    Args:
        text (string): Story Data

    Returns:
        boolean
    """
    text = nlp(text)
    for topic in keyword_list:
        if topic in [token.lemma_.lower() for token in text]:
            return keyword_list[topic]
    return None


def get_entities(text):
    people, organisations, locations = entities(text)
    people = [each_string.lower() for each_string in people]
    organisations = [each_string.lower() for each_string in organisations]
    locations = [each_string.lower() for each_string in locations]
    # check known word vocabulary for entities
    with open(os.path.join(dirname, '../../../graph_db_generator/entities.pickle'), "rb") as target:
        entity_dict = pickle.load(target)
    words = word_tokenize(text)
    for word in words:
        if word.lower() in entity_dict:
            if entity_dict[word.lower()] == 'Person' and word.lower() not in people:
                people.append(word.lower())
            elif word.lower() not in organisations:
                organisations.append(word.lower())
        # look for non-subsidery products
        if word.lower() in products:
            comp = products[word.lower()]
            if comp.lower() not in organisations:
                organisations.append(comp.lower())
    return people, organisations, locations


def link_finder(text):
    people, organisations, locations = get_entities(text)
    link = is_topic_of_interest(text)
    prediction = predictor.predict(text)
    all_entities = people + organisations
    if type(link) != type(None):
        for row in prediction["verbs"]:
            flag1 = False
            flag2 = False
            results = re.findall(r"\[.*?\]", row["description"])
            for res in results:
                if "ARG0" in res:
                    for entity in all_entities:
                        if entity in res:
                            flag1 = True
                if "ARG1" in res:
                    for entity in all_entities:
                        if entity in res:
                            flag2 = True
            if flag1 and flag2:
                link = getAllInflections(nlp(row["verb"])[0].lemma_)["VBG"][0]
                break
    return people, organisations, locations, link
