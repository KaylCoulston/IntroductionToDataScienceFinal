import nltk
import pickle
from ReviewsData import *
from GetFeatures import *

def main():
    review_file = open("review_data.pickle", "rb")
    r = pickle.load(review_file)
    review_file.close()

    summary = r.Summarize()

    ratings_dist = summary["RatingsDist"]
    ratings_dist.plot()

    asins_dist = summary["AsinsDist"]
    asins_dist.plot(10)

    most_common_topics = r.GetMostCommonTopics(20)

    most_common_topics.plot(20, title="Number of Reviews Containing 20 Most Common Words")

main()
