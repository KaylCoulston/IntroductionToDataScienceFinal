import gzip
import nltk

# Keys are :
# ['reviewerID', 'asin', 'reviewerName', 'helpful', 'unixReviewTime', 'reviewText', 'overall', 'reviewTime', 'summary']

num_reviews = 1000

def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

def catagorize_by_key(lst, key):
    items = {}
    for r in lst:
        if key in r:
            if r[key] in items:
                items[r[key]].append(r)
            else:
                items[r[key]] = [r]
    return items


reviews_file = parse("reviews_Video_Games_5.json.gz")
reviews = []

for r in reviews_file:
    if len(reviews) == num_reviews and num_reviews != -1:
        break
    reviews.append(r)

#keys_list = [reviews[0].keys()]
#for r in reviews:
    #if r.keys() != keys_list[-1]:
        #keys_list.append(r.keys())
    #print r.keys()

#overall = [i["overall"] for i in reviews]
#print overall
#print sum(overall) / len(overall)

#print keys_list
#print reviews[0].keys()
#print reviews[0]
#print type(reviews[0])

by_product = catagorize_by_key(reviews, "asin")

for key in by_product.keys():
    print key
    print len(by_product[key])

#print catagorize_by_key(reviews, "reviewerName").keys()
#sorted_by_score = catagorize_by_key(reviews, "overall")
#print sorted_by_score[1.0]

#tokens = nltk.word_tokenize(sorted_by_score[1.0][0]["reviewText"])
#print tokens

#porter = nltk.PorterStemmer()
#for r in sorted_by_score[1.0]:
    #t = nltk.text.Text(nltk.tokenize.word_tokenize(r["reviewText"].lower()))
    #print nltk.pos_tag(t)
