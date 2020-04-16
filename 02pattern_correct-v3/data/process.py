import pandas as pd
data = pd.read_excel("all.xlsx")["弹体质量"]
data2 = []
for d in data:
    if type(d) == float:
        continue
    else:
        data2.append(d.replace(' ',''))
print(len(data2))
# data = pd.DataFrame()
# data['sentence'] = data2
# writer = pd.ExcelWriter('alldata.xlsx')
# data.to_excel(writer, 'page_1', float_format='%.10f',index=None)
# writer.save()
# writer.close()
