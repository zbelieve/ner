import pandas as pd
import random
data = pd.read_excel("alldata.xlsx")["sentence"]
data2 = []
for d in data:
    data2.append(d)
random.shuffle(data2)
data = pd.DataFrame()
data['sentence'] = data2
writer = pd.ExcelWriter('alldata.xlsx')
data.to_excel(writer, 'page_1', float_format='%.10f',index=None)
writer.save()
writer.close()
