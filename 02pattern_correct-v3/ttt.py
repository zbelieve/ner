x = ['x','y']
y = ['x','e','r']
for w in y:
    if w in x:
        print(w)
print(x[-1])
import jieba
jieba.suggest_freq('kg/m3', tune=True)
jieba.suggest_freq('m/s', tune=True)