from utils import *
from Instance import *
import pandas as pd
from Senetnce import *
from ppattern import Pattern
import numpy as np
from gensim import matutils
data = pd.read_excel("/data2.xlsx")["弹体质量"]
data2 = []
data3 = []

# 处理data的空行
for d in data:
    # 如果是空格就跳过
    if type(d) == float:
        print(d)
        continue
    else:
        data2.append(d.replace(' ',''))
print(len(data2))

# 将sentence转为实例
def senToInstan(S,ListInstance):
    sentence = S
    e1List = sentence.e1_List
    e2List = sentence.e2_List
    for e1 in e1List:
        for e2 in e2List:
            f=0
            # e1在前面
            if e1[1]<=e2[1]:
                for word in sentence.segSentence2[e1[1]+1:e2[1]]:
                    # 判断了这两个词是不是在一句话中
                    if word in ['.', '。', ';', ';']:
                        f = 1
                        break
                if f==0:
                    # 添加一个实例
                    instance = Instance(S,e1,e2,flag = 0)
                    ListInstance.append(instance)
            # e2在后面
            if e1[1]>e2[1]:
                for word in sentence.segSentence2[e2[1]+1:e1[1]]:
                    if word in['.','。',';',';']:
                        f = 1
                        break
                if f==0:
                    instance = Instance(S, e1, e2,flag = 1)
                    ListInstance.append(instance)
    return ListInstance
ListSentence1 = []
ListInstance1= []
for d in data2[2:3]:
      ListSentence1.append(s)
      senToInstan(s,ListInstance1)


###### 创造模板
ListInstance2 = []
for d in data2[0:1]:
      s2 = Sentence(d)
      senToInstan(s2,ListInstance2)
pattern = []
for I in ListInstance2:
    if I.e1[1]<31:
        pattern.append(I)
patternLast = []
for I in pattern:
    patt = Pattern(I.sentence,I.bef,I.bet,I.aft,I.e1,I.e2,I.flag)
    patternLast.append(pattern)
    # print(patt.befVec)

for L1 in ListInstance1:
    for L2 in pattern:
        befVec = np.dot(matutils.unitvec(L1.befVec), matutils.unitvec(L2.befVec))
        betVec = np.dot(matutils.unitvec(L1.betVec), matutils.unitvec(L2.betVec))
        aftVec = np.dot(matutils.unitvec(L1.aftVec), matutils.unitvec(L2.aftVec))
        vec = 0.2*befVec+0.6*betVec+0.2*aftVec
        if vec>0.95:
            print(L1.str)
            print(L1.e1)
            print(L1.e2)
            break
# print(np.dot(matutils.unitvec(a), matutils.unitvec(b)))





