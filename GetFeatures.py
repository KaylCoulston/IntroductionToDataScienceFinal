from datetime import datetime
from nltk.classify import apply_features
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.text import Text
from nltk.tokenize import word_tokenize
from random import shuffle
import gzip
import nltk
import nltk.classify.util
import pickle
import string

porter = nltk.PorterStemmer()
wnl = nltk.WordNetLemmatizer()

# Same as reviewdata class but takes one review
def get_most_common_words(rvw, amount):
    all_words = []
    for words in word_tokenize(rvw["summary"]):
        all_words.append(words.lower())

    stop_words = set(stopwords.words("english"))
    all_words = [words for words in all_words if not words in stop_words]

    punctuation = list(string.punctuation)
    all_words = [words for words in all_words if not words in punctuation]

    all_words = [porter.stem(t) for t in all_words]
    all_words = [wnl.lemmatize(t) for t in all_words]

    all_words = nltk.FreqDist(all_words)
    return all_words.most_common(amount)

def get_most_common_taggs(reviews):
    all_words = []
    for rvw in reviews:
        tagged_text = nltk.pos_tag(word_tokenize(rvw["reviewText"]))
        for tagged in tagged_text:
            if tagged[1] == "X": #JJ" or tagged[1] == "JJR" or tagged[1] == "JJS":
                all_words.append(tagged[0])

    all_words = nltk.FreqDist(all_words)
    return all_words.most_common(20)

def word_feats(words):
    return dict([(word, True) for word in words])

def label_review(review):
    if review["overall"] < 3.0:
        return (review, "neg")
    elif review["overall"] == 3.0:
        return (review, "neutral")
    else:
        return (review, "pos")

# get_features takes a review and generates features for it. additionlly it
# labels the review "pos" "neutral" or "neg". The function returns a tuple of
# the form (review_features, label) where review_features is a dictionary.
def get_features(review):
    f = {}
    #f.update(word_feats(review["nltkText"]))

    # helpful field is tuple with helpful[0] being yes and helpful[1] being no.
    # the field counts the number of times the review was flagged as helpful vs
    # not helpful
    # This extracts the helpful field into a single feature with
    # helpful = y(es) if there are more yes answers than no
    # helpful = u(nknown) if there are the same number of yes and no answers
    # helpful = n(0) if there are less yes answers than no
    if review["helpful"][0] > review["helpful"][1]:
        f["helpful"] = "y"
    elif review["helpful"][0] == review["helpful"][1]:
        f["helpful"] = "u"
    else:
        f["helpful"] = "n"

    #f["score"] = review["overall"]

    #I think we need to better filter words from the nltkText rather than just
    #adding every one. We could also construct our own preliminary classifier
    #that takes the words of a review and outputs some sort of score as an
    #aggregate.
    most_common = [w[0] for w in get_most_common_words(review, 30)]
    #most_common = [w[0] for w in get_most_common_taggs(review)]
    f.update(word_feats(most_common))

    # Seeing if most common bigrams as features works better
    #bigrams = nltk.bigrams(review["nltkText"])
    #bigram_freq = nltk.FreqDist(bigrams)

    ##print bigram_freq.most_common(5)
    #for b in bigram_freq.most_common(10):
    #    f.update({(b[0], True)})

    return f


