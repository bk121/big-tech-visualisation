from add_articles_to_graph.nlp.topic_classifier.setup.tokenizer import tokenizer
import os
import sys
import pickle
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

classifier_f = open(
    "add_articles_to_graph/nlp/topic_classifier/setup/pickle/classifier.pickle",
    "rb",
)
classifiers = pickle.load(classifier_f)
classifier_f.close()

classifier = classifiers[0]


def topic(text):
    if text == "":
        return ""
    return classifier.predict([text])[0]
