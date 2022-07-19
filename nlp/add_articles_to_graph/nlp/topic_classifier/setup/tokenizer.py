import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")
stopwords = list(STOP_WORDS)

def tokenizer(sentence):
    punct = string.punctuation  # get list of punctuation.
    doc = nlp(sentence)  # prepare text for spacy.
    tokens = []
    for token in doc:
        """
        Iterate through the words in the text.
        """
        if token.lemma_ != "-PRON-":
            """
            Ignore pronouns.
            """
            temp = token.lemma_.lower().strip()
            # lemmantize, lowercase, and remove extra characters.
        else:
            temp = token.lower_
            # don't lemmantize pronouns, just lowercase them.
        tokens.append(temp)  # add to list of tokens.
    cleaned_tokens = []
    for token in tokens:
        """
        Iterate through all tokens.
        """
        if token not in stopwords and token not in punct:
            """
            Remove stopwords from tokens.
            """
            cleaned_tokens.append(token)
    return cleaned_tokens
