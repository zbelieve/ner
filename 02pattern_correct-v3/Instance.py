import gensim
import numpy as np
wordTvec = gensim.models.KeyedVectors.load_word2vec_format('croups/outervector2.txt', binary=True, unicode_errors="ignore")
class Instance():
    def __init__(self, sentence=None,segSentence2 =None,segSentenceNumG = None,e1=None,e2 = None,flag = None,isTrue=0):

        self.str = sentence
        self.strSeg1 = segSentence2
        self.strSeg2 = segSentenceNumG
        self.flag = flag
        self.e1 = e1["e1"]
        self.e2 = e2["e2"]
        self.e1_index = e1["index1"]
        self.e2_index = e2["index2"]
        self.bef = None
        self.bet = None
        self.aft = None
        self.flag = flag
        self.conf = None
        self.segIns()
        self.befVec = self.IwordTvec(self.bef)
        self.betVec = self.IwordTvec(self.bet)
        self.aftVec = self.IwordTvec(self.bef)
        self.isTrue = isTrue

    # 获取相加的词向量
    def IwordTvec(self,strList):
        Vec = np.zeros(50)
        for s in strList:
            if s in ["质量","重量","重","靶标","混凝土靶标","弹丸","弹体","靶","混凝土靶",""]:
                Vec = 2*wordTvec[s]+Vec
            else:
                Vec = wordTvec[s] + Vec
        return Vec
    # 根据实体切分
    def segIns(self):
        str = self.strSeg2
        # 说明self.e1在前面，self.e2在后面

        if self.flag==0:
            i = self.e1_index
            self.bef = str[:self.e1_index]
            self.bet = str[self.e1_index + 1:self.e2_index]
            self.aft = str[self.e2_index + 1:]
            i = 0
            fuHao1 = []
            for word in self.bef:
                if i<len(self.bef) and word in ['.','。',';',';']:
                    fuHao1.append(i)
                i=i+1
            if len(fuHao1)>0:
                self.bef = str[fuHao1[-1]+1:self.e1_index]
            fuHao2 = []
            j =0
            for word in self.aft:
                if j < len(self.aft) and word in ['.', '。', ';', ';']:
                    fuHao2.append(j)
                j = j + 1
            if len(fuHao2) > 0:
                self.aft = str[self.e2_index+1:self.e2_index+1+fuHao2[0]]

        # 说明self.e1在后面，self.e2在前面
        else:
            self.bef = str[:self.e2_index]
            self.bet = str[self.e2_index+1:self.e1_index]
            self.aft = str[self.e1_index+1:]
            i = 0
            fuHao1 = []
            for word in self.bef:
                if i < len(self.bef) and word in ['.', '。', ';', ';']:
                    fuHao1.append(i)
                i = i + 1
            if len(fuHao1) > 0:
                self.bef = str[fuHao1[-1] + 1:self.e2_index]
            fuHao2 = []
            j = 0
            for word in self.aft:
                if j < len(self.aft) and word in ['.', '。', ';', ';']:
                    fuHao2.append(j)
                j = j + 1
            if len(fuHao2) > 0:
                self.aft = str[self.e1_index + 1:self.e1_index + 1 + fuHao2[0]]

    def PwordTvec(self, strList):
        Vec = np.zeros(50)
        for s in strList:
            Vec = wordTvec[s] + Vec
        return Vec





