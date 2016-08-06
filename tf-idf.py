from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def get_corpus(filename):
    corpus = []
    f = open(filename,"r")
    for line in f:
        corpus.append(line.replace("\n","").split(" ")[2].replace(","," "))
    return corpus


def tfidf(corpus):
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)
    a = x.toarray()
    print vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(a)
    return tfidf.toarray()


def euclidean_metric(vector1,vector2):
    sqDiffVector = vector1 - vector2
    sqDiffVector = sqDiffVector ** 2
    sqDistance = sqDiffVector.sum()
    distance = sqDistance ** 0.5
    return distance

def classification():
    f = open("dataset/raw/dim_items.txt", "r")
    label = {}
    for line in f:
        arr = line.replace("\n","").split(" ")
        label[arr[0]] = arr[1]
    return label

def item_matcher_pair():
    f = open("dataset/raw/dim_fashion_matchsets.txt", "r")
    label = classification()
    matcher_pair = []
    index = 0
    for line in f:
        if index == 3:
            break
        index += 1
        p = []
        arr = line.replace("\n","").split(" ")
        pairs = arr[1].split(";")
        for pair in pairs:
            item = pair.split(",")[0]
            p.append(label[item])
        matcher_pair.append(p)
    return matcher_pair
