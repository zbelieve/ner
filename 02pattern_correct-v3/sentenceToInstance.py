import json
from Instance import Instance
from croups.SenetnceCropus import Sentence
import codecs
import numpy as np
from gensim import matutils

train_data = json.load(open('croups/pattern_data_me.json',encoding='utf-8'))
test_data = json.load(open('croups/test2_data_me.json',encoding='utf-8'))


def senToInstan(sentence =None,segSentence2=None,segSentenceNumG=None,e1_list=None,e2_list = None,ListInstance=None):
    # sentence = S
    e1List = e1_list
    e2List = e2_list
    for e1 in e1List:
        for e2 in e2List:
            f=0
            # e1在前面
            if e1["index1"]<=e2["index2"]:
                for word in segSentenceNumG[e1["index1"]+1:e2["index2"]]:
                    # 判断了这两个词是不是在一句话中
                    if word in ['.', '。', ';', ';']:
                        f = f+1
                        if f>=2:
                            break
                if f==0 or f==1:
                    # 添加一个实例
                    instance = Instance(sentence=sentence,segSentence2 =segSentence2,segSentenceNumG = segSentenceNumG,e1=e1,e2 = e2 ,flag = 0)
                    ListInstance.append(instance)
            # e2在后面
            if e1["index1"]>e2["index2"]:
                for word in segSentenceNumG[e2["index2"]+1:e1["index1"]]:
                    if word in['.','。',';',';']:
                        f = f+1
                        if f>=2:
                            break
                if f==0 or f ==1:
                    instance = Instance(sentence=sentence,segSentence2 =segSentence2,segSentenceNumG = segSentenceNumG,e1=e1,e2 = e2 ,flag = 1)
                    ListInstance.append(instance)
    return ListInstance
ListInstance =  []
for w in train_data:
    senToInstan(sentence =w["sentence"],segSentence2=w["segSentence2"],segSentenceNumG=w["segSentenceNumG"],e1_list=w["e1_List"],e2_list = w["e2_List"],ListInstance=ListInstance)
pattern = []
with codecs.open('bef/pattern_ins.json', 'w', encoding='utf-8') as f:
    # 每一个s都是一个instance
    for s in ListInstance:
        pattern.append(
            {
                "str": s.str,
                "strSeg1":s.strSeg1,
                "strSeg2": s.strSeg2,
                "flag": s.flag,
                "e1":s.e1,
                "e2": s.e2,
                "e1_index": s.e1_index,
                "e2_index": s.e2_index,
                "bef": s.bef,
                "bet": s.bet,
                "aft": s.aft,
                "flag": s.flag,
                "conf": s.conf,
                "is_True": s.isTrue
            }
        )
    json.dump(pattern, f, indent=4, ensure_ascii=False)



ListInstance2 =  []
test = []
for w in test_data:
    Ins = senToInstan(sentence =w["sentence"],segSentence2=w["segSentence2"],segSentenceNumG=w["segSentenceNumG"],e1_list=w["e1_List"],e2_list = w["e2_List"],ListInstance=ListInstance2)
with codecs.open('bef/test_ins2.json', 'w', encoding='utf-8') as f:
    # 每一个s都是一个instance
    for s in ListInstance2:
        test.append(
            {
                "str": s.str,
                "strSeg1":s.strSeg1,
                "strSeg2": s.strSeg2,
                "flag": s.flag,
                "e1":s.e1,
                "e2": s.e2,
                "e1_index": s.e1_index,
                "e2_index": s.e2_index,
                "bef": s.bef,
                "bet": s.bet,
                "aft": s.aft,
                "flag": s.flag,
                "conf": s.conf,
                "is_True": s.isTrue
            }
        )
    json.dump(test, f, indent=4, ensure_ascii=False)

# ListInstance是模板，ListInstance2是测试
for L1 in ListInstance2:
    for L2 in ListInstance:
        # if L2.isTrue==1:
        befVec = np.dot(matutils.unitvec(L1.befVec), matutils.unitvec(L2.befVec))
        betVec = np.dot(matutils.unitvec(L1.betVec), matutils.unitvec(L2.betVec))
        aftVec = np.dot(matutils.unitvec(L1.aftVec), matutils.unitvec(L2.aftVec))
        vec = 0.1*befVec+0.8*betVec+0.1*aftVec
        if vec>0.99:
            print(L1.str)
            print(L1.e1)
            print(L1.e2)
