# import re
# b = []
# str  = "混凝土素混凝土"
# liststr = ["素混凝土","混凝土"]
# for l in liststr:
#     for a in re.finditer(l, str):
#         b.append(a.span())
# print(b)
# def sortStr(b):
#     L = []
#     for one in b:
#
#         L.append((one[0],one[1],one[1]-one[0]))
#     # 遍历所有数组元素
#     n = len(b)
#     for i in range(n):
#         # Last i elements are already in place
#         for j in range(0, n - i - 1):
#             if L[j][2] > L[j + 1][2]:
#                 L[j], L[j + 1] = L[j + 1], L[j]
#     L2 = []
#     for one in L:
#         L2.append((one[0],one[1]))
#     return L2

print(len("弹丸头部为卵形(弹形系数为3),长130mm,直径20mm,重0.250kg.靶体为混凝土材料,强度为76.6MPa.为了防止弹丸高速冲击作用造成混凝土靶体的过度破碎,靶体采用高和直径都相对较大的圆柱体,并用弧形钢板紧箍。"))
