import re
import tqdm
import codecs
import json
import pandas as pd
from SenetnceCropus import Sentence

# data = pd.read_excel("../data/all.xlsx")["弹体质量"]\
#        +pd.read_excel("../data/all.xlsx")["弹体重量"]
data = pd.read_excel("../data/data3.xlsx")["弹体质量"]
print(data)
data2 = []
data3 = []

# 将所有的质量数据放入data2中，其中去除了空行和空格
for d in data:
    if type(d) == float:
        continue
    else:
        data2.append(d.replace(' ',''))

ListSentence = []
ListInstance = []
# 将其中的 e1_List，e2_List，sentence（原始句子），segSentence2（正确分词后），segSentenceNumG（将质量数字转成NumG）保存
for d in data2:
      s = Sentence(d)
      ListSentence.append(s)
      data3.append(s.segSentence2)
      print(s.segSentence2)

all_data = []
with codecs.open('all_data_me.json', 'w', encoding='utf-8') as f:
    for d in data2:
        s = Sentence(d)
        all_data.append(
            {
                "e1_List": [({
                    "e1": w[0],
                    "index1":w[1]})for w in s.e1_List],
                "e2_List": [({
                    "e2": w[0],
                    "index2": w[1]}) for w in s.e2_List],
                "sentence": s.sentence,
                "segSentence2": s.segSentence2,
                "segSentenceNumG": s.segSentenceNumG
            }
        )
    json.dump(all_data, f, indent=4, ensure_ascii=False)

# resc = re.compile('(([0-9]\d*\.?\d*)(G|g|KG|kg|t|T))')
# i = 0
## 将弹丸质量进行替换
# for d1 in data3:
#     j = 0
#     for d2 in d1:
#         if i<len(data3) and len(data3[i]) and re.findall(resc, d2):
#             data3[i][j] = 'numsKg'
#         j=j+1
#     i=i+1
# for d1 in data3:
#     print(d1)
# print(data3)
# import multiprocessing
# from gensim.models import Word2Vec
# word2vec_path = 'corpusSegDone_2.model'
# out_vector = 'outervector2.txt'
# model = Word2Vec(sentences=data3, size=50, window=4, min_count=0,
#                      workers=multiprocessing.cpu_count(),iter=1)
# model.save(word2vec_path)
# model = Word2Vec.load(word2vec_path)
# model.wv.save_word2vec_format(out_vector, binary=True)
# print(model.wv.similarity('重', '弹丸'))
# print(model.wv.similarity('重量', '质量'))
# print(model.wv.similarity('弹体', '穿甲弹'))
# print(model.wv.similarity('混凝土板靶', '质量'))
# word_vector = zip(model.wv.vocab, model.wv.vectors)
# output = open('./w2v.txt', 'w', encoding='utf-8')
# for item in word_vector:
#     vector = [str(v) for v in item[1]]
#     vector = ' '.join(vector)
#     output.write(item[0]+'\t'+vector.strip()+'\n')
# output.close()



