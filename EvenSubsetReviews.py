from ReviewsData import *
import random
import json
import gzip

# Keep in mind this will give a random sample every time so only run this once
# then use the resulting data

subset = []

num_reviews = -1
r = ReviewsData("reviews_Video_Games_5.json.gz", num_reviews)

# This is the number of 2.0 star reviews in data set. There are the least
# number of 2.0 star reviews in the whole dataset
"""
reviews_per_score = 13663
for score in [1.0, 2.0, 3.0, 4.0, 5.0]:
    rvws = r.GetReviewsOfScore(score)

    even_subset += random.sample(rvws, reviews_per_score)
"""

#CommonTopics = r.GetMostCommonTopics(40)

for rvw in r.reviews:
	for word in word_tokenize(rvw["reviewText"]):
		if word == "story" or word == "level" or word == "multiplayer" or word == "version" or word == "gameplay":
			subset.append(rvw)
			break

outfile = gzip.open("reviews_Video_Games_5_Topics.json.gz", "w")

for r in subset:
    outfile.write(json.dumps(r) + "\n")
