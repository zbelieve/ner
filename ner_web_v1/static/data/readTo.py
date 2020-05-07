import pandas as pd
import re
# 弹体：弹体类型Dtype,弹体材料Dmaterials，弹体材料强度DmaterialsStrength;，弹头形状Dshape，CRH Dcrh，弹体直径Ddiameter，弹体长度Dlength，弹体质量Dweight
# 着靶参数：弹体速度Zspeed，命中角Zangle
# 靶标：靶标材料种类Btype，靶标厚度Bthickness,靶标抗压强度Bstrength，靶标材料密度Bdensity，靶标配筋率Bratio
# 效应：侵彻深度Xdepth，贯穿Xpenetrate
data0 = pd.read_excel("datanew.xlsx")["段落"][0:100]
data1 = pd.read_excel("datanew.xlsx")["发射炮类型"][0:100]
data2 = pd.read_excel("datanew.xlsx")["侵彻深度"][0:100]
data3 = pd.read_excel("datanew.xlsx")["弹体类型"][0:100]
data4 = pd.read_excel("datanew.xlsx")["弹体材料"][0:100]
data5 = pd.read_excel("datanew.xlsx")["弹体质量"][0:100]
data6 = pd.read_excel("datanew.xlsx")["弹头形状"][0:100]
data7 = pd.read_excel("datanew.xlsx")["CRH"][0:100]
data8 = pd.read_excel("datanew.xlsx")["弹体直径"][0:100]
data9 = pd.read_excel("datanew.xlsx")["弹体长度"][0:100]
data10 = pd.read_excel("datanew.xlsx")["弹体速度"][0:100]
data11 = pd.read_excel("datanew.xlsx")["靶标材料种类"][0:100]
data12 = pd.read_excel("datanew.xlsx")["靶标材料密度"][0:100]
data13 = pd.read_excel("datanew.xlsx")["靶标厚度"][0:100]
data14 = pd.read_excel("datanew.xlsx")["靶标抗压强度"][0:100]
data15 = pd.read_excel("datanew.xlsx")["弹体材料强度"][0:100]
data16 = pd.read_excel("datanew.xlsx")["命中角"][0:100]
data17 = pd.read_excel("datanew.xlsx")["靶标配筋率"][0:100]
data18 = pd.read_excel("datanew.xlsx")["贯穿"][0:100]

# print(data0[1:2])
# 清除空格等,如果是指定字符串，会有指定操作
def clean(str,flag=0):
    seg = ""
    for w in str:
        # 统一字符格式
        if w == ",":
            w = "，"
        if w == ":":
            w = "："
        # 去掉空格
        if w != " ":
            seg = seg + w
    print()
    # 这个是配合像弹体类型这一类字段用的
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



# 转化为BIOE,data1是字符串，b1是[（1，3）,(3,6)]这样的，是某个特定字符的位置
def ToBIOE(data1,b1=None,b2=None,b3=None,b4=None,b5=None,b6=None,b7=None,b8=None,b9=None,b10=None,b11=None,b12=None,b13=None,b14=None,b15=None,b16=None,b17=None,b18=None):
    BIOE = []
    for i in range(0,len(data1)):
        BIOE.append("O")

    # 发射炮类型
    if b1!=None:
        print(b1)
        for d in b1:
            BIOE[d[0]] = "B-F"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-F"
    # 侵彻深度
    if b2 != None:
        for d in b2:
            BIOE[d[0]] = "B-Xdepth"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Xdepth"
    # 弹体类型
    if b3 != None:
        for d in b3:
            BIOE[d[0]] = "B-Dtype"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dtype"
    # 弹体材料
    if b4 != None:
        for d in b4:
            BIOE[d[0]] = "B-Dmaterials"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dmaterials"
    # 弹体质量
    if b5 != None:
        for d in b5:
            BIOE[d[0]] = "B-Dweight"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dweight"
    # 弹头形状
    if b6 != None:
        for d in b6:
            BIOE[d[0]] = "B-Dshape"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dshape"
    # CRH
    if b7 != None:
        for d in b7:
            BIOE[d[0]] = "B-Dcrh"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dcrh"
    # 弹体直径
    if b8 != None:
        for d in b8:
            BIOE[d[0]] = "B-Ddiameter"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Ddiameter"
    # 弹体长度
    if b9 != None:
        for d in b9:
            BIOE[d[0]] = "B-Dlength"
            for j in range(d[0]+1,d[1]):
                BIOE[j] = "I-Dlength"
    # 弹体速度
    if b10 != None:
        for d in b10:
            BIOE[d[0]] = "B-Zspeed"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Zspeed"

    # 靶标材料种类
    if b11 != None:
        for d in b11:
            BIOE[d[0]] = "B-Btype"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Btype"
    # 靶标材料密度
    if b12 != None:
        for d in b12:
            BIOE[d[0]] = "B-Bdensity"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Bdensity"
    # 靶标厚度
    if b13 != None:
        for d in b13:
            BIOE[d[0]] = "B-Bthickness"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Bthickness"
    # 靶标抗压强度
    if b14 != None:
        for d in b14:
            BIOE[d[0]] = "B-Bstrength"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Bstrength"
    # 弹体材料强度
    if b15 != None:
        for d in b15:
            BIOE[d[0]] = "B-DmaterialsStrength"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-DmaterialsStrength"
    # 命中角
    if b16 != None:
        for d in b16:
            BIOE[d[0]] = "B-Zangle"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Zangle"
    # 靶标配筋率
    if b17 != None:
        for d in b17:
            BIOE[d[0]] = "B-Bratio"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Bratio"
    # 贯穿
    if b18 != None:
        for d in b18:
            BIOE[d[0]] = "B-Xpenetrate"
            for j in range(d[0] + 1, d[1]):
                BIOE[j] = "I-Xpenetrate"
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
        b11 = None
        b12 = None
        b13 = None
        b14 = None
        b15 = None
        b16 = None
        b17 = None
        b18 = None
        # 指定词语clean后的字符串
        print(data1[i])
        print(type(data1[i]))
        print(data2[i])
        print(type(data2[i]))
        if type(data1[i]) == str:
            data11c = clean(data1[i],1)
            b1 = sortStr(index_of(data00, data11c))
        if type(data2[i]) == str:
            data22c = clean(data2[i], 1)
            b2 = sortStr(index_of(data00, data22c))

        if type(data3[i]) == str:
            data33c = clean(data3[i], 1)
            b3 = sortStr(index_of(data00, data33c))
        if type(data4[i]) == str:
            data44c = clean(data4[i], 1)
            b4 = sortStr(index_of(data00, data44c))
        if type(data5[i]) == str:
            data55c = clean(data5[i], 1)
            b5 = sortStr(index_of(data00, data55c))

        if type(data6[i]) == str:
            data66c = clean(data6[i], 1)
            b6 = sortStr(index_of(data00, data66c))

        if type(data7[i]) == str:
            data77c = clean(data7[i], 1)
            b7 = sortStr(index_of(data00, data77c))

        if type(data8[i]) == str:
            data88c = clean(data8[i], 1)
            b8 = sortStr(index_of(data00, data88c))

        if type(data9[i]) == str:
            data99c = clean(data9[i], 1)
            b9 = sortStr(index_of(data00, data99c))

        if type(data10[i]) == str:
            data1010c = clean(data10[i], 1)
            b10 = sortStr(index_of(data00, data1010c))
        if type(data11[i]) == str:
            print(i)
            data1111c = clean(data11[i],1)
            b11 = sortStr(index_of(data00, data1111c))
        if type(data12[i]) == str:
            data1212c = clean(data12[i], 1)
            b12 = sortStr(index_of(data00, data1212c))

        if type(data13[i]) == str:
            data1313c = clean(data13[i], 1)
            b13 = sortStr(index_of(data00, data1313c))
        if type(data14[i]) == str:
            data1414c = clean(data14[i], 1)
            b14 = sortStr(index_of(data00, data1414c))
        if type(data15[i]) == str:
            data1515c = clean(data15[i], 1)
            b15 = sortStr(index_of(data00, data1515c))

        if type(data16[i]) == str:
            data1616c = clean(data16[i], 1)
            b16 = sortStr(index_of(data00, data1616c))

        if type(data17[i]) == str:
            data1717c = clean(data17[i], 1)
            b17 = sortStr(index_of(data00, data1717c))

        if type(data18[i]) == str:
            data1818c = clean(data18[i], 1)
            b18 = sortStr(index_of(data00, data1818c))
        if b1==None and b2==None and b3==None and b4==None and b5==None and b6==None and b7==None and b8==None and b9==None and b10==None and b11==None and b12==None and b13==None and b14==None and b15==None and b16==None and b17==None and b18==None:
            continue
        BIOE = ToBIOE(data1=data00,b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,b6=b6,b7=b7,b8=b8,b9=b9,b10=b10,b11=b11,b12=b12,b13=b13,b14=b14,b15=b15,b16=b16,b17=b17,b18=b18)
        all.append(data00)
        all.append(data00arr)
        all.append(BIOE)
        T = []
        for i in range(0,len(data00arr)):
            T.append((data00arr[i],BIOE[i]))
        all.append(T)
        All.append(all)
        print()
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











