# -*- coding: utf-8 -*-

from pymongo import MongoClient 
from konlpy.tag import Kkma, Mecab, Twitter
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
import numpy as np

client = MongoClient('localhost', 27017)
mongo_collections = client['articles']['major']
_db_data_test = mongo_collections.find({'article_datetime': {'$regex': '.*20190124.*'}})
_db_data_training = mongo_collections.find({'article_datetime': {'$regex': '.*20190124.*'}})

twitter = Twitter()
def tokenizer(raw, stopword=[]):
    return [
            word for word, tag in twitter.pos(
                raw, 
                norm=True, 
                stem=True
                )
            if len(word) > 1 and word not in stopword
            ]
def main():
    title_data = []
    for _data in _db_data_training:
        title_data.append(_data['title'])
    vectorize = TfidfVectorizer(
        tokenizer=tokenizer,
        min_df=2,
        sublinear_tf=True
        )
    X = vectorize.fit_transform(title_data)
    features = vectorize.get_feature_names()
    for tokens in _db_data_test:
        srch = [t for t in tokens['title'] if t in features]
    srch_dtm = np.asarray(X.toarray())[:, [
        vectorize.vocabulary_.get(i) for i in srch]]
    score = srch_dtm.sum(axis=1)
    f = open('/home/ubuntu/venv_article/articlesite/tfidf_result.txt', 'w', encoding='utf8')
    for i in score.argsort()[::-1]:
        f.write('{} / score : {}'.format(title_data[i], score[i]))
