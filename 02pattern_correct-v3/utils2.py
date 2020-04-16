def segAll(self):
    index = []
    dex = []
    i = 0
    for x in self.segSentence2:
        if i < len(x) and x == '。' or x == ';' or x == '。' or x == '；':
            dex.append(x)
            dex.append(i)
            index.append(dex)
            i = i + 1
    for e1 in self.e1_List:
        for e2 in self.e2_List:
            bef = self.segSentence2[0:e1[1]]
            bet = self.segSentence2[e1[1] + 1:e2[1]]
            aft = self.segSentence2[e2[1] + 1:]

