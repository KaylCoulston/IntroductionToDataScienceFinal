import gzip
import string
import nltk
from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime

"""
The review is parsed in as an array of dictionaries of reviews.  The vast
majority of reviews in the array have these keys. There are a couple that
have other fields but I don't think they are substantially different enough
that we need to really care right now since they should still have the fields
we need.

Review Keys = ['reviewerID', 'asin', 'reviewerName', 'helpful',
'unixReviewTime', 'reviewText', 'overall', 'reviewTime', 'summary', 'featureWords']

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

        #self.SanitizeText()
        #self.AddNltkReviewText()

    def AddNltkReviewText(self):
        for rvw in self.reviews:
            t = {"nltkText": Text(word_tokenize(" ".join(rvw["saniText"]).lower()))}
            #t = {"nltkText": Text(word_tokenize(rvw["reviewText"].lower()))}
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
        if type(score) is list:
            lst = []
            for s in score:
                if type(s) is not float:
                    raise TypeError("Error: Score should be 1.0, 2.0, etc, and should be a float")

                lst += self.CatagorizeByKey("overall")[s]
            return lst

        elif type(score) is not float:
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

    def GetMostCommonAsin(self, amount):
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

    def SanitizeText(self):
        for rvw in self.reviews:
            all_words = []
            for words in word_tokenize(rvw["reviewText"]):
                all_words.append(words.lower())

            stop_words = set(stopwords.words("english"))
            all_words = [words for words in all_words if not words in stop_words]

            punctuation = list(string.punctuation)
            all_words = [words for words in all_words if not words in punctuation]

            rvw["saniText"] = all_words

    def Summarize(self):
        ratings = [r["overall"] for r in self.reviews]
        reviewer_ids = [r["reviewerID"] for r in self.reviews]
        helpful_score = [r["helpful"][0] - r["helpful"][1] for r in self.reviews]
        times = [r["unixReviewTime"] for r in self.reviews]
        asins = [r["asin"] for r in self.reviews]
        review_lengths = [len(r["reviewText"]) / 100 for r in self.reviews]

        #>>> fdist = FreqDist(word.lower() for word in word_tokenize(sent))
        ratings_dist = nltk.FreqDist(ratings)
        reviewer_ids_dist = nltk.FreqDist(reviewer_ids)
        asins_dist = nltk.FreqDist(asins)
        helpful_score_dist = nltk.FreqDist(helpful_score)
        review_lengths_dist = nltk.FreqDist(review_lengths)

        """
        print reviewer_ids_dist.most_common(10)
        #print ratings_dist.pformat()
        #print reviewer_ids_dist.pformat()
        #print asins_dist .pformat()
        print "ratings_dist plot"
        print ratings_dist.plot(50)
        #print helpful_tags_dist
        print "asins_dist plot"
        print asins_dist.plot(50)
        print "reviewer_ids plot"
        print reviewer_ids_dist.plot(50)
        """

        summary = {}
        summary["NumReviews"] = len(self.reviews)
        summary["NumItems"] = len(asins)
        summary["EarliestReview"] = datetime.fromtimestamp(min(times))
        summary["MostRecentReview"] = datetime.fromtimestamp(max(times))
        summary["RatingsDist"] = ratings_dist.pformat()
        r_lengths = [len(r["reviewText"]) for r in self.reviews]
        summary["AvgReviewLength"] = sum(r_lengths) / float(len(r_lengths))
        summary["AvgReviewsPerUser"] = float(reviewer_ids_dist.N()) / float(reviewer_ids_dist.B())
        summary["AvgReviewsPerItem"] =  float(asins_dist.N()) / float(asins_dist.B())
        summary["AvgNetHelpful"] = sum(helpful_score) / float(len(helpful_score))
        summary["MostCommonAsins"] = asins_dist.most_common(5)
        summary["MostCommonReviewerIDS"] = reviewer_ids_dist.most_common(5)
        summary["RvwLengthDistInHundredsOfChars"] = review_lengths_dist.items()

        review_lengths_dist.plot(1000)

        #Review Keys = ['reviewerID', 'asin', 'reviewerName', 'helpful',
        #'unixReviewTime', 'reviewText', 'overall', 'reviewTime', 'summary']

        for key in summary.keys():
            print key + ": "
            print summary[key]

        return summary

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
