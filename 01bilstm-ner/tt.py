import re
s = "后弹体明显跳弹，\r\t弹体穿入防护钢靶中。"
x = re.findall("\r\t",s)
print(s.split("\r\t"))
print(x)

