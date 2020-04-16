import re
import tqdm
import codecs
import json
import pandas as pd
from SenetnceCropus import Sentence


# data = pd.read_excel("../data/data_me_test.xlsx")["sentence"][5:15]
data = pd.read_excel("../data/data_me_test.xlsx")["sentence"]
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
with codecs.open('test2_data_me.json', 'w', encoding='utf-8') as f:
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





