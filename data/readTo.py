import pandas as pd
import re
data0 = pd.read_excel("data3.xlsx")["段落"][0:43]
data1 = pd.read_excel("data3.xlsx")["弹丸类型或名称"]
data2 = pd.read_excel("data3.xlsx")["弹体材料"]
data3 = pd.read_excel("data3.xlsx")["弹丸质量"]
data4 = pd.read_excel("data3.xlsx")["弹丸直径"]
data5 = pd.read_excel("data3.xlsx")["弹丸长度"]
data6 = pd.read_excel("data3.xlsx")["弹丸速度"]
data7 = pd.read_excel("data3.xlsx")["靶标种类"]
data8 = pd.read_excel("data3.xlsx")["靶标密度"]
data9 = pd.read_excel("data3.xlsx")["发射炮类型"]
data10 = pd.read_excel("data3.xlsx")["侵彻深度"]
# print(data0[1:2])
# 清除空格等,如果是指定字符串，会有指定操作
def clean(str,flag=0):
    seg = ""
    for w in str:
        if w == ",":
            w = "，"
        if w == ":":
            w = "："
        if w != " ":
            seg = seg + w
    if flag==1:
        seg = seg.split("==")
    return seg

# 寻找字符匹配的位置，返回[（1，3）,(3,6)]
def index_of(str,liststr):
    b = []
    for l in liststr:
        for a in re.finditer(l, str):
            b.append(a.span())
    return b

# b是[(107, 112), (95, 99), (108, 112)]这样的,这是给这个数组的相减后的长度排序，从小到大，这样字符长的就能掩盖掉字符短的
def sortStr(b):
    L = []
    for one in b:

        L.append((one[0],one[1],one[1]-one[0]))
    # 遍历所有数组元素
    n = len(b)
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if L[j][2] > L[j + 1][2]:
                L[j], L[j + 1] = L[j + 1], L[j]
    L2 = []
    for one in L:
        L2.append((one[0],one[1]))
    return L2



# 转化为BIOE,data1是字符串，b1是[（1，3）,(3,6)]这样的，是某个特定字符的
def ToBIOE(data1,b1=None,b2=None,b3=None,b4=None,b5=None,b6=None,b7=None,b8=None,b9=None,b10=None):
    BIOE = []
    for i in range(0,len(data1)):
        BIOE.append("O")
    # 弹丸类型或名称
    if b1!=None:
        print(b1)
        for d in b1:
            BIOE[d[0]] = "B-Dname"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dname"
    # 弹体材料
    if b2 != None:
        for d in b2:
            BIOE[d[0]] = "B-Dmaterial"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Material"
    # 弹丸质量
    if b3 != None:
        for d in b3:
            BIOE[d[0]] = "B-Dweight"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dweight"
    # 弹丸直径
    if b4 != None:
        for d in b4:
            BIOE[d[0]] = "B-Ddiameter"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Ddiameter"
    # 弹丸长度
    if b5 != None:
        for d in b5:
            BIOE[d[0]] = "B-Dlength"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dlength"
    # 弹丸速度
    if b6 != None:
        for d in b6:
            BIOE[d[0]] = "B-Dspeed"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dspeed"
    # 靶标种类
    if b7 != None:
        for d in b7:
            BIOE[d[0]] = "B-Btype"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Btype"
    # 靶标密度
    if b8 != None:
        for d in b8:
            BIOE[d[0]] = "B-Bdensity"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Bdensity"
    # 发射炮类型
    if b9 != None:
        for d in b9:
            BIOE[d[0]] = "B-F"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-F"
    # 侵彻深度
    if b10 != None:
        for d in b10:
            BIOE[d[0]] = "B-Height"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Height"
    return BIOE


# 将字符串转换为数组
def toArray(strs):
    arr = []
    for w in strs:
        arr.append(w)
    return arr

All = []
for i in range(0,len(data0)):
    all = []
    if type(data0[i])!=float:
        # 句子clean后的字符串
        data00 = clean(data0[i])
        data00arr = toArray(data00)
        b1 = None
        b2 = None
        b3 = None
        b4 = None
        b5 = None
        b6 = None
        b7 = None
        b8 = None
        b9 = None
        b10 = None
        # 指定词语clean后的字符串
        # if type(data1[i])!=float:
        #     data11 = clean(data1[i],1)
        #     b1 = sortStr(index_of(data00, data11))
        # if type(data2[i]) != float:
        #     data22 = clean(data2[i], 1)
        #     b2 = sortStr(index_of(data00, data22))
        #
        # if type(data3[i]) != float:
        #     data33 = clean(data3[i], 1)
        #     b3 = sortStr(index_of(data00, data33))

        if type(data4[i]) != float:
            data44 = clean(data4[i], 1)
            b4 = sortStr(index_of(data00, data44))

        # if type(data5[i]) != float:
        #     data55 = clean(data5[i], 1)
        #     b5 = sortStr(index_of(data00, data55))
        #
        # if type(data6[i]) != float:
        #     data66 = clean(data6[i], 1)
        #     b6 = sortStr(index_of(data00, data66))
        #
        # if type(data7[i]) != float:
        #     data77 = clean(data7[i], 1)
        #     b7 = sortStr(index_of(data00, data77))
        #
        # if type(data8[i]) != float:
        #     data88 = clean(data8[i], 1)
        #     b8 = sortStr(index_of(data00, data88))
        #
        # if type(data9[i]) != float:
        #     data99 = clean(data9[i], 1)
        #     b9 = sortStr(index_of(data00, data99))
        #
        # if type(data10[i]) != float:
        #     data1010 = clean(data10[i], 1)
        #     b10 = sortStr(index_of(data00, data1010))

        BIOE = ToBIOE(data1=data00,b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,b6=b6,b7=b7,b8=b8,b9=b9,b10=b10)
        all.append(data00)
        all.append(data00arr)
        all.append(BIOE)
        T = []
        for i in range(0,len(data00arr)):
            T.append((data00arr[i],BIOE[i]))
        all.append(T)
        All.append(all)
# for w in All:
#     for x in w:
#         print(x)
#     print()
with open("train_data.txt",'w',encoding="utf-8",) as f:
    i = 0
    for w in All:
        if w[3]:
            print(w[3])
            i= i+1
            for w2 in w[3]:
                f.write(w2[0])
                f.write('\t')
                f.write(w2[1])
                f.write('\n')

        f.write('\n')











