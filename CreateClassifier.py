import gzip
import nltk
import nltk
import nltk.classify.util
import pickle
import string

from datetime import datetime
from nltk.classify import apply_features
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.text import Text
from nltk.tokenize import word_tokenize
from random import shuffle

from ReviewsData import *
from GetFeatures import *

def main():
    num_reviews = -1

    #To get the most common topics we I ran this:
    """
    r = ReviewsData("reviews_Video_Games_5.json.gz", num_reviews)

    r.Summarize()
    data = [label_review(rvw) for rvw in r.reviews]
    print r.GetMostCommonTopics(40)
    """

    #Classify based off of summaries
    r = ReviewsData("reviews_Video_Games_5.json.gz", num_reviews)
    r.Summarize()

    data = [label_review(rvw) for rvw in r.reviews]
    shuffle(data)

    num_reviews = len(data)
    print get_features(data[0][0])
    num_reviews = int(num_reviews * 0.75)
    trainfeats = apply_features(get_features, data[:num_reviews])
    testfeats = apply_features(get_features, data[num_reviews:])

    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()

    save_file = open("review_classifier.pickle", "wb")
    pickle.dump(classifier, save_file)
    save_file.close()

"""
# Classification using words in review

    feats = []
    cutoffs = []
    for idx, score in enumerate([[1.0, 2.0], [4.0, 5.0]]):
        rev = r.GetReviewsOfScore(score)
        if idx == 0:
            feats.append([(word_feats(words["nltkText"]), "neg") for words in rev])
            cutoffs.append(len(feats[idx])*3/4)
        elif idx == 1:
            feats.append([(word_feats(words["nltkText"]), "pos") for words in rev])
            cutoffs.append(len(feats[idx])*3/4)

    trainfeats = []
    testfeats = []
    for idx,f in enumerate(feats):
        trainfeats += f[:cutoffs[idx]] + f[:cutoffs[idx]]
        testfeats += f[cutoffs[idx]:] + f[cutoffs[idx]:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()
    """

main()
