#  -*- coding: utf-8 -*-
#已获取搭配列表中与测试商品最相似的商品
#TODO 根据该商品匹配到搭配列表中的搭配类目对，获取与之搭配的商品和对应类目，并根据这些信息计算与之较为相近的商品
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def m_intersection(a,b):
    """
    取交集
    """
    return list(set(a).intersection(set(b)))


def tfidf(corpus):
    """
    获取语料库中每一个句子的tf-idf值
    :param corpus: 语料库
    """
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)
    a = x.toarray()
    # print vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(a)
    return tfidf.toarray()


def euclidean_metric(vector1,vector2):
    """
    计算欧式距离
    :param vector1:向量1
    :param vector2: 向量2
    """
    sqDiffVector = vector1 - vector2
    sqDiffVector = sqDiffVector ** 2
    sqDistance = sqDiffVector.sum()
    distance = sqDistance ** 0.5
    return distance

def classification():
    """
    获取每个item的类目
    """
    f = open("dataset/raw/dim_items.txt", "r")
    label = {}
    for line in f:
        arr = line.replace("\n","").split(" ")
        label[arr[0]] = arr[1]
    return label


def infomation():
    """
    获取每一个item的标题
    :return:
    """
    f = open("dataset/raw/dim_items.txt", "r")
    info = {}
    for line in f:
        arr = line.replace("\n","").split(" ")
        info[arr[0]] = arr[2]
    return info



def item_matcher_pair():
    """
    获取达人搭配数据的搭配类目对，和商品对（仍需处理）
    :return:
    """
    f = open("dataset/raw/dim_fashion_matchsets.txt", "r")
    label = classification()
    matcher_pair = []
    matcher_pair2 = []
    for line in f:
        p = []
        p2 = []
        arr = line.replace("\n","").split(" ")
        pairs = arr[1].split(";")
        for i in pairs:
            p2.append(i)
        for pair in pairs:
            item = pair.split(",")[0]
            p.append(label[item])
        matcher_pair.append(p)
        matcher_pair2.append(p2)
    return matcher_pair,matcher_pair2


def fashion_items():
    """
    获取达人搭配商品对
    :return:
    """
    a,b = item_matcher_pair()
    items = []
    for i in b:
        for j in i:
            arr = j.split(',')
            for k in arr:
                items.append(k)
    return set(items)


def same_label_item(label,labels,fashion_items):
    """
    获取指定目的分类的达人搭配商品表中的商品
    :param item:
    :param label:
    :return:
    """
    items = []
    for k,v in labels.items():
        if v == label:
            items.append(k)
    return m_intersection(items,fashion_items)


def sorted_result(item,item_label,labels,infos,fashion_items):
    items = same_label_item(item_label,labels,fashion_items)
    if len(items) >= 20000:
        return []
    corpus = []
    for i in items:
        corpus.append(infos[i])
    tf_idf = tfidf(corpus)
    items_info = {}
    for i in range(len(tf_idf)):
        items_info[items[i]] = tf_idf[i]
    for i in range(len(tf_idf)):
        items_info[items[i]] = euclidean_metric(items_info[item],items_info[items[i]])
    return sorted(items_info.items(),key=lambda x:x[1],reverse=False)


def tfidf_items(items,infos):
    """
    获取指定商品集的tfidf
    :param items:
    :param infos:
    :return:
    """
    corpus = []
    for i in items:
        corpus.append(infos[i])
    tf_idf = tfidf(corpus)
    items_info = {}
    for i in range(len(tf_idf)):
        items_info[items[i]] = tf_idf[i]
    return items_info


def most_similr_items(item,items_info):
    """
    获取与指定商品最相近的商品
    :param item:
    :param items_info:
    :return:
    """
    most_items_info = {}
    for k in items_info:
        most_items_info[k] = euclidean_metric(items_info[item],items_info[k])
    return sorted(most_items_info.items(),key=lambda x:x[1])


if __name__ == "__main__":
    labels = classification()
    infos = infomation()
    fashion_items = fashion_items()
    # a,b = item_matcher_pair()
    items = same_label_item('33',labels,fashion_items)
    items.append('1417')
    items_info = tfidf_items(items,infos)
    print most_similr_items('1417',items_info)