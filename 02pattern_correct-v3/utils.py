import re
import jieba,jieba.posseg as jp


# startJVM(getDefaultJVMPath(), "-Djava.class.path=G:\DM\lp\pkg\hanlp\hanlp-1.5.0.jar;G:\DM\lp\pkg\hanlp",
#          "-Xms1g",
#          "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
# HanLP = JClass('com.hankcs.hanlp.HanLP')
# CustomDictionary = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
# 读取质量
# def regquality(strs):
#     res1 = re.compile('(([0-9]\d*\.?\d*)(kg/m3|g|m/s|mm|kg|m|t|T))')
#     res2 = re.compile('(([0-9]\d*\.?\d*)-([0-9]\d*\.?\d*)(kg/m3|g|m/s|mm|kg|m))')
#     res3 = re.compile('(([0-9]\d*\.?\d*)(kg/m3|g|m/s|mm|kg|m)-([0-9]\d*\.?\d*)(kg/m3|g|m/s|mm|kg|m))')
#     res4 = re.compile('(([0-9]\d*\.?\d*)±([0-9]\d*\.?\d*)(kg/m3|g|m/s|mm|kg|m))')
#     segNum2 = re.findall(res2, strs)
#     segNum3 = re.findall(res3, strs)
#     segNum4 = re.findall(res4, strs)
#     segNum1 = re.findall(res1, strs)
#     segNumList = []
#     other = []
#     for seg in segNum1:
#         x = strs.split(seg[0])
#         if x[0].endswith('-') or x[1].startswith('-') or x[0].endswith('±') or x[1].startswith('±'):
#             continue
#         if seg[2] in ['g','kg','KG','G','t']:
#             segStr = seg[0]
#             segNumList.append(segStr)
#     for seg in segNum2:
#         if seg[3] in ['g', 'kg', 'KG', 'G', 't']:
#             segStr = seg[0]
#             segNumList.append(segStr)
#     for seg in segNum3:
#         if seg[4] in ['g', 'kg', 'KG', 'G', 't']:
#             segStr = seg[0]
#             segNumList.append(segStr)
#     for seg in segNum4:
#         if seg[3] in ['g', 'kg', 'KG', 'G', 't']:
#             segStr = seg[0]
#             segNumList.append(segStr)
#
#     return segNumList


# 读取主体
# def regSub(strs):
#     file = open("subject.txt", encoding='UTF-8')
#     dataSub = []
#     regs = []
#     for line in file.readlines():
#         lineN = line.split("\n")[0]
#         dataSub.append(lineN)
#     for word in dataSub:
#         res1 = re.compile(word)
#         reg = re.findall(res1,strs)
#         if len(reg):
#             regs.append(reg)
#     return regs



# def segNum(strs,nums):
#     for num in nums:
#         CustomDictionary.insert(num, "numqu 1000")
#     return HanLP.segment(strs)
s = "为了分析某种结构助推钻地弹的侵彻效果，本文作者首先进行了无助推结构，即纯动能钻地弹侵彻试验，" \
    "试验的基本状态为：弹丸质量为41.28kg，41.28kg弹丸直径为125mm，要求弹丸着靶速度为560m/s，混凝土靶为C35的圆柱形素混凝土靶，" \
    "靶面直径2.4m，长4m，靶体密度为2360kg/m3。试验中弹丸实际着靶速度为563m/s，锥形弹坑深度为499mm，侵彻深度为1507mm。"

def forword_Match(text):
    file = open("subject.txt", encoding='UTF-8')
    Dict = []
    for line in file.readlines():
        lineN = line.split("\n")[0]
        Dict.append(lineN)
    '''前向最大匹配'''
    word_list = []
    pi = 0  # 初始位置
    # 找出字典中的最长的词的长度
    m = max([len(word) for word in Dict])
    while pi != len(text):
        n = len(text[pi:])  # 当前指针到字符串末尾的长度
        if n < m:
            m = n
        for index in range(m, 0, -1):  # 从当前 pi 起取 m 个汉字作为词
            if text[pi:pi + index] in Dict:
                word_list.append(text[pi:pi + index])
                pi = pi + index  # 根据词的长度修改指针pi
                break
    print('/'.join(word_list))





# SegWord = segWord(s)
# a,b= regquality2(SegWord)
# print(a)
# print(b)
# c = regSub2(b)
# print(c)
# d = regDan(c)
# print("xxxxxxxxxxxxx")
# print(d)






