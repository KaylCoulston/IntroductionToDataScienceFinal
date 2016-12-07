import gzip
import string
import nltk
from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

"""
The review is parsed in as an array of dictionaries of reviews.  The vast
majority of reviews in the array have these keys. There are a couple that
have other fields but I don't think they are substantially different enough
that we need to really care right now since they should still have the fields
we need.

Review Keys = ['reviewerID', 'asin', 'reviewerName', 'helpful',
'unixReviewTime', 'reviewText', 'overall', 'reviewTime', 'summary']

Also the key "nltkText" will be added which points to a ntlk Text instance for
review text which has been lowercased
"""
class ReviewsData:
    def __init__(self, reviews_filename, max_reviews = -1):
        self.reviews = []

        reviews_file = gzip.open(reviews_filename, 'r')
        for line in reviews_file:
            if len(self.reviews) == max_reviews and max_reviews != -1:
                break
            self.reviews.append(eval(line))

        reviews_file.close()

        self.AddNltkReviewText()

    def AddNltkReviewText(self):
        for rvw in self.reviews:
            t = {"nltkText": Text(word_tokenize(rvw["reviewText"].lower()))}
            rvw.update(t)

    def CatagorizeByKey(self, key):
        items = {}
        for rvw in self.reviews:
            if key in rvw:
                if rvw[key] in items:
                    items[rvw[key]].append(rvw)
                else:
                    items[rvw[key]] = [rvw]
        return items

    def GetReviewsOfScore(self, score):
        if type(score) is not float:
            raise TypeError("Error: Score should be 1.0, 2.0, etc, and should be a float")

        return self.CatagorizeByKey("overall")[score]

    def GetPossibleKeys(self):
        return self.reviews[0].keys()

    def GetNltkReviewTextArray(self):
        return [rvw["nltkText"] for rvw in self.reviews]

    def GetSubsetByKeys(self, key_list):
        subset = []
        for rvw in self.reviews:
            item = {}
            for k in key_list:
                item[k] = rvw[k]
            subset.append(item)

        return subset

    def GetMostCommonWords(self, amount):
        all_words = []
        for rvw in self.reviews:
            for words in word_tokenize(rvw["reviewText"]):
                all_words.append(words.lower())

        stop_words = set(stopwords.words("english"))
        all_words = [words for words in all_words if not words in stop_words]

        punctuation = list(string.punctuation)
        all_words = [words for words in all_words if not words in punctuation]

        all_words = nltk.FreqDist(all_words)
        return all_words.most_common(amount)

    def GetMostCommonAsin(self):
        all_asin = []
        for rvw in self.reviews:
            all_asin.append(rvw["asin"])

        all_asin = nltk.FreqDist(all_asin)
        return all_asin.most_common(amount)

    def LinkWordsToReview(self, common):
        reviews = []
        for rvw in self.reviews:
            for words in word_tokenize(rvw["reviewText"]):
                if words in common:
                    reviews.append(rvw["asin"])

        return reviews

def word_feats(words):
    return dict([(word, True) for word in words])

def main():
    r = ReviewsData("reviews_Video_Games_5.json.gz", 10000)

    feats = []
    cutoffs = []
    for score in [1.0, 2.0, 3.0, 4.0, 5.0]:
        rev = r.GetReviewsOfScore(score)
        feats.append([(word_feats(words["nltkText"]), str(score)) for words in rev])
        cutoffs.append(len(feats[int(score-1.0)])*3/4)

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
"""


"""
    #Some examples for how to use things:
    print "Possible Keys: "
    print r.GetPossibleKeys()
    print

    print "Subsetted by keys 'overall' and 'nltkText'"
    print r.GetSubsetByKeys(["overall", "nltkText"])[1]

    print r.CatagorizeByKey("asin").keys()
    print

    one_star = r.GetReviewsOfScore(1.0)
    print "One Star Reviews Text: "
    for r in one_star:
        print r["reviewText"]
"""
main()
