from utils import *
class Sentence():
    def __init__(self, sentence=None):
        self.sentence = sentence
        # 分词
        seg1 = self.segWord(sentence)
        self.segSentence1 = seg1
        # 输出是识别质量之后返回quality，返回一个就是处理好质量的分好词的字符串
        # 就是里面本来有些句子是数字和单位分开的，现在的话放到一个句子里面，就是数字和单位没有分开
        # quality里面除了第一个是字符外，第二个是对应句子里面的索引
        quality, strs = self.regquality2(seg1)
        self.segSentence2 = strs
        # 识别的是object里面的主语，然后在里面再挑选弹丸
        Sub = self.regSub2(strs)
        Dan = self.regDan(Sub)
        # 第一个是字符，第二个是对应句子里面的索引
        self.e2_List = quality
        self.e1_List = Dan

        self.vec1 = None
        self.vec2 = None
        self.bef = None
        self.bet = None
        self.aft = None
        self.entity1 = None
        self.entity2 = None

    # 将句子切分为数组
    # 如果有些特殊字符切分不出来，需要改造jieba
    def segWord(self, strs):
        fileSub = open("../spo/subject.txt", encoding='UTF-8')
        fileObj = open("../spo/object.txt", encoding='UTF-8')
        fileP = open("../spo/p.txt", encoding='UTF-8')
        self.freq(fileSub)
        self.freq(fileObj)
        self.freq(fileP)
        word_list = jieba.cut(strs,cut_all=False)
        segWord = []
        for word in word_list:
            segWord.append(word)
        return segWord

    def freq(self,file):
        for line in file.readlines():
            lineN = line.split("\n")[0]
            jieba.suggest_freq(lineN.strip(), tune=True)


    # 如果匹配到数字后面跟着单位则是质量,输入是segWord（）切分后的数组
    def regquality2(self,strs1):
        strs = []
        for w in strs1:
            strs.append(w)
        Dict = ['KG', 'G', 'T', 'kg', 'g', 't']
        res1 = re.compile('([0-9]\d*\.?\d*)')
        res2 = re.compile('(([0-9]\d*\.?\d*)(G|g|KG|kg|t|T))')
        i = 0
        quality = []
        for word in strs:
            q = []
            if i < len(strs) and re.findall(res1, word) and strs[i + 1] in Dict:
                temp1 = word
                temp2 = strs[i + 1]
                temp = temp1 + temp2
                q.append(temp)
                q.append(i)
                quality.append(q)
                strs[i] = temp
                strs.pop(i + 1)
            # 有些时候分词器会把290g这样的词分出来，这时候上面一步就分不出来了
            elif re.findall(res2, strs[i]):
                sp = re.findall(res2, strs[i])
                spt = re.split(sp[0][0],word)
                if len(spt[1])==0:
                    q.append(strs[i])
                    q.append(i)
                    quality.append(q)

            i = i + 1
        return quality, strs

    # 输入的是经过分词并且质量重组后的句子，识别主语，并返回主语的索引
    def regSub2(self,strs):
        file = open("subject.txt", encoding='UTF-8')
        Dict = []

        Sub = []
        for line in file.readlines():
            lineN = line.split("\n")[0]
            Dict.append(lineN)
        i = 0
        for word in strs:
            if i < len(strs) and word in Dict:
                Sub1 = []
                Sub1.append(word)
                Sub1.append(i)
                Sub.append(Sub1)
            i = i + 1
        return Sub

    # 识别弹丸,输入是主语识别后的主语列表
    def regDan(self,sub):
        file = open("subjectDan.txt", encoding='UTF-8')
        DictDan = []
        for line in file.readlines():
            lineN = line.split("\n")[0]
            DictDan.append(lineN)
        Dan = []
        for seg in sub:
            if seg[0] in DictDan:
                Dan.append(seg)
        return Dan




