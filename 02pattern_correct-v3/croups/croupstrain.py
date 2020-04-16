import re
from tqdm import tqdm
import codecs
import json
import pandas as pd
from SenetnceCropus import Sentence
import json
sentence = []
train_data = json.load(open('all_data_me.json',encoding='utf-8'))
for w in train_data:
    sentence.append(w["segSentenceNumG"])
for w in sentence:
    print(w)

import multiprocessing
from gensim.models import Word2Vec
word2vec_path = 'corpusSegDone_2.model'
out_vector = 'outervector2.txt'
model = Word2Vec(sentences=sentence, size=50, window=4, min_count=0,
                     workers=multiprocessing.cpu_count(),iter=1)
model.save(word2vec_path)
model = Word2Vec.load(word2vec_path)
model.wv.save_word2vec_format(out_vector, binary=True)
print(model.wv.similarity('重', '弹丸'))
print(model.wv.similarity('重量', '质量'))
print(model.wv.similarity('弹体', '穿甲弹'))
print(model.wv.similarity('混凝土板靶', '质量'))
word_vector = zip(model.wv.vocab, model.wv.vectors)
output = open('./w2v.txt', 'w', encoding='utf-8')
for item in word_vector:
    vector = [str(v) for v in item[1]]
    vector = ' '.join(vector)
    output.write(item[0]+'\t'+vector.strip()+'\n')
output.close()



