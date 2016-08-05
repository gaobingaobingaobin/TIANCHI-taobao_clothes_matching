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
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(a)
    return tfidf.toarray()