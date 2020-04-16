import jieba
from gensim import corpora,models,similarities
from collections import defaultdict
import numpy as np
import os
import copy
documents = []
name = []
def sm(url):
    # 1、读取文档
    newurl = "./"+url+".txt"
    newurls=open(newurl,encoding='GBK').read()
    # 2、对要计算的文档进行分词
    datal = jieba.cut(newurls)
    # text_create(url, "|".join(datal))
    # 3、对分词完的数据进行整理为指定格式（整理成字符串+空格形式然后存入document中）
    datall = ""
    for i in datal:
        datall += i + " "
    # datall这时候是一个空格加分词的字符串
    documents.append(datall)
    # documents这时候是一个列表，每一个位置是一个datall
    #print(documents)
    name.append(url)


# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg

def text_create(name, msg):
    if os.path.exists(name+"jieba.txt"):
        os.remove(name+"jieba.txt")
        desktop_path = "./"  # 新创建的txt文件的存放路径
        full_path = desktop_path + name + 'jieba.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write(msg)  # msg也就是下面的Hello world!
    else:
        desktop_path = "./"  # 新创建的txt文件的存放路径
        full_path = desktop_path + name + 'jieba.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write(msg)  # msg也就是下面的Hello world!


def main():
    # 1、读取文档
    sm("d1")
    sm("d2")
    sm("d3")
    sm("d4")
    sm("d5")
    sm("d6")
    sm("d7")
    sm("d8")
    sm("d9")
    sm("d10")
    sm("d11")
    sm('d13')
    sm("d14")
    sm("d15")
    sm("d16")
    # 建立一个语料库,每一个doucment是一个分词加空格的字符串，然后document.split()进行切分后最里面的列表就是每一个是一个分词
    texts=[[word for word in document.split()] for document in documents]
    #print(texts)
    #建立字典
    frequency=defaultdict(int)
    # 4、 计算词语的频率
    for text in texts:
        for word in text:
            # 字典对应的key值增加1
            frequency[word]+=1
    # 6、通过语料库将文档的词语进行建立词典
    dictionary=corpora.Dictionary(texts)
    dictionary.save("./dict.txt")   #可以将生成的词典进行保存
    # 7、加载要对比的文档
    doc3c="d17"
    doc3="./"+doc3c+".txt"
    d3=open(doc3,encoding='GBK').read()
    data3=jieba.cut(d3)
    data31=""
    for i in data3:
        data31+=i+" "
    # 8、将要对比的文档通过doc2bow转化为稀疏向量
    new_xs=dictionary.doc2bow(data31.split())
    #print(new_xs)
    # 9、对语料库进一步处理，得到新语料库，对其中的每个词进行处理，转化为稀疏向量
    corpus=[dictionary.doc2bow(text)for text in texts]
    # 10、将新语料库通过tf-idf model 进行处理，得到tfidf
    # TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一份文件对于所在的一个语料库中的重要程度。
    # 字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。
    tfidf=models.TfidfModel(corpus)
    # 11、通过token2id得到特征数（字典里面的键的个数）
    featurenum=len(dictionary.token2id.keys())
    # print(featurenum)
    # 12、稀疏矩阵相似度，从而建立索引，特征数和稀疏向量建立索引
    index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featurenum)
    # 13、得到最终相似结果，将new_xs也就是要比对的文档传入，这儿得到的就是相似结果,查询相似的百分比
    sim=index[tfidf[new_xs]]
    # 下面就是排序，拿出前三个最相似的文档
    sim1=sorted(sim,reverse=True)
    sim2=sim1[0:3:1]
    s1=np.where(sim == sim2[0])
    s2=np.where(sim == sim2[1])
    s3 = np.where(sim == sim2[2])
    print(sim)
    print(sim1)
    print(sim2)
    for a in s1[0]:
        ss1=a
    for a in s2[0]:
        ss2 = a
    for a in s3[0]:
        ss3=a
    print("第一匹配文档是",name[ss1])
    print("第二匹配文档是",name[ss2])
    print("第三匹配文档是",name[ss3])





if __name__ == "__main__":
    main()