import nltk
import pickle
from ReviewsData import *
from GetFeatures import *
import matplotlib.pyplot as plt

def main():
    #To get the most common topics we I ran this:
    review_file = open("review_data.pickle", "rb")
    r = pickle.load(review_file)
    review_file.close()
    """
    r = ReviewsData("reviews_Video_Games_5_Even_Subset_Small.json.gz")
    """

    summary = r.Summarize()

    #r.Summarize()
    most_common_topics_dist = r.GetMostCommonTopics()

    most_common_topics_dist.plot(20)

    """
    sum_lengths = summary["ReviewLengthsDist"].items()
    print sum_lengths
    x = [l[0] for l in sum_lengths]
    y = [l[1] for l in sum_lengths]

    plt.plot(x, y, color='b')
    plt.ylabel("Number of Reviews")
    plt.xlabel("Length in Words")
    plt.title("Review Lengths")
    plt.show()

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
    summary["RatingsDist"] = ratings_dist
    summary["ReviewerIdsDist"] = reviewer_ids_dist
    summary["AsinsDist"] = asins_dist
    summary["HelpfulScoreDist"] = helpful_score_dist
    summary["ReviewLengthsDist"] = review_lengths_dist
    summary["SummaryLengthDist"] = summary_lengths_dist
    """

main()
