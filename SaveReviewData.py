import nltk
import pickle
from ReviewsData import *
from GetFeatures import *

def main():
    r = ReviewsData("reviews_Video_Games_5_Topics.json.gz")

    save_file = open("review_data.pickle", "wb")
    pickle.dump(r, save_file)
    save_file.close()
