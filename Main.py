import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.classify import apply_features

from ReviewsData import *

# Same as reviewdatat class but takes one review
def get_most_common_words(rvw, amount):
    all_words = []
    for words in word_tokenize(rvw["reviewText"]):
        all_words.append(words.lower())

    stop_words = set(stopwords.words("english"))
    all_words = [words for words in all_words if not words in stop_words]

    punctuation = list(string.punctuation)
    all_words = [words for words in all_words if not words in punctuation]

    all_words = nltk.FreqDist(all_words)
    return all_words.most_common(amount)

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

    f["score"] = review["overall"]

    # I think we need to better filter words from the nltkText rather than just
    # adding every one. We could also construct our own preliminary classifier
    # that takes the words of a review and outputs some sort of score as an
    # aggregate.
    most_common = [w[0] for w in get_most_common_words(review, 10)]
    f.update(word_feats(most_common))

    return f

def main():
    num_reviews = 1000
    r = ReviewsData("reviews_Video_Games_5.json.gz", num_reviews)
    data = [label_review(rvw) for rvw in r.reviews]

    print get_features(data[0][0])
    trainfeats = apply_features(get_features, data[num_reviews/2:])
    testfeats = apply_features(get_features, data[:num_reviews/2])

    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()

# Classification using words in review
"""
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