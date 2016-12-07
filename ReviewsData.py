import gzip
import nltk
from nltk.text import Text
from nltk.tokenize import word_tokenize

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

def main():
    r = ReviewsData("reviews_Video_Games_5.json.gz", 100)

"""
    Some examples for how to use things:

    print "Possible Keys: "
    print r.GetPossibleKeys()
    print

    print "Subsetted by keys 'overall' and 'nltkText'"
    print r.GetSubsetByKeys(["overall", "nltkText"])[0]

    print r.CatagorizeByKey("asin").keys()
    print

    one_star = r.GetReviewsOfScore(1.0)
    print "One Star Reviews Text: "
    for r in one_star:
        print r["reviewText"]
"""

main()
