import pandas as pd
import random
import json
import codecs
pattern_data = json.load(open('../croups/all_data_me.json',encoding='utf-8'))

data2 = []
for d in pattern_data:
    data2.append(d)
random.shuffle(data2)

pattern = []
with codecs.open('../croups/pattern_data_me.json', 'w', encoding='utf-8') as f:
    for d in data2[0:5]:
        pattern.append(
            d
        )
    json.dump(pattern, f, indent=4, ensure_ascii=False)

test = []
with codecs.open('../croups/test_data_me.json', 'w', encoding='utf-8') as f:
    for d in data2[5:15]:
        test.append(
            d
        )
    json.dump(test, f, indent=4, ensure_ascii=False)
