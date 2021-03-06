import nltk
import pickle
from ReviewsData import *
from GetFeatures import *

def main():
    #To get the most common topics we I ran this:
    review_file = open("review_data.pickle", "rb")
    r = pickle.load(review_file)
    review_file.close()

    classifier_file = open("review_classifier.pickle", "rb")
    classifier = pickle.load(classifier_file)
    classifier_file.close()

    for i in range(10):
        data = label_review(r.reviews[i])
        print "Review Summary: ",
        print r.reviews[i]["summary"]
        print "Classifier Probability: "
        prob = classifier.prob_classify(get_features(data[0]))
        print "Pos: ",
        print prob.prob("pos")
        print "Neutral: ",
        print prob.prob("neutral")
        print "Neg: ",
        print prob.prob("neg")
        print "Actual: ",
        print data[1]
        print


main()
