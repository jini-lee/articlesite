# -*- coding: utf-8 -*-

from pymongo import MongoClient
from gensim.models.doc2vec import Doc2Vec, LabeledSentence, TaggedDocument
from gensim.test.utils import get_tmpfile
from konlpy.tag import Kkma, Okt 
import sys, os, re
import multiprocessing
import datetime

client = MongoClient('localhost', 27017)
mongo_collections = client['articles']['major']
_db_data_test = mongo_collections.find({'article_datetime': {'$regex': '.*20190124.*'}, 'press': '한겨레'})
_db_data_training = mongo_collections.find({'article_datetime': {'$regex': '.*20190124.*'}})
# _db_data_training = mongo_collections.find({'article_datetime': {'$regex': '.*20190128.*'}, 'press': {'$ne' : '한겨레'}})
# _db_data_training = mongo_collections.find()

pos_tagger = Okt()
kkma = Kkma()
class LabeledLineSentence(object):
    def __init__(self, collections):
        self.collections = collections
    def __iter__(self):
        for collection in self.collections:
            yield LabeledSentence(words=self.tokenize(collection['title']), tags=[collection['title']])
    def tokenize(self, collection):
        # sentence = collection['title'] + \
        #         ' '.join(kkma.sentences(collection['article_body'])[:3])
        return [t[0] for t in pos_tagger.pos(collection, norm=True, stem=True) if t[1] == 'Noun']

def start_training():
    documents = LabeledLineSentence(_db_data_training)
    model = Doc2Vec(documents, dm=1, vector_size=7, window=3, epochs=5, worker=8, alpha=0.025, min_alpha=0.025)
    # model_time = datetime.datetime.now().strftime('_%Y%m%d_%H%M')
    os.remove('/tmp/doc2vec.model')
    fname = get_tmpfile('doc2vec.model')
    model.save(fname)

def start_test():
    model = Doc2Vec.load('/tmp/doc2vec.model')
    f = open('/home/ubuntu/venv_article/articlesite/test_result.txt', 'w', encoding='utf8')
    for idx, data in enumerate(_db_data_test):
        tokens = [t[0] for t in pos_tagger.pos(data['title'], norm=True, stem=True) if t[1] == 'Noun']
        n_vector = model.infer_vector(tokens)
        sims = model.docvecs.most_similar([n_vector])
        f.write('criterior : {} infer_vector : {} \n'.format(data['title'], tokens))
        for sim in sims:
            f.write('result : {}, accur : {:f}\n'.format(sim[0], sim[1]))
        f.write('--------------------------------------\n\n')
