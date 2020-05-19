# ner
# 一些nlp方面的练手项目

# 01bilstm-ner
## 项目介绍
这是一个keras构建ner并识别的项目
## 内容介绍
data:
1.data中xlsx结尾的是标记数据（因为没找到合适的标记工具）
2.readTo就是将xlsx转换为标记的语料
3.model就是保存的模型

ner:是程序主体，识别21个标签
nerpre：是用模型进行预测用的
## 后期不定期更新

# 02 pattern_correct-v3
## 项目说明
这是一个利用传统的bootstrapping方法利用模板进行判断的关系抽取项目
这个前面走了一些弯路，由于是传统方法所以代码比较多，第一次做这个，做的有点乱
总体就是利用模板去判断两个句子是否相似
## 功能说明
1.croups里面主要就是切分句子，然后用word2evc来进行训练
2.data是数据以及数据预处理
## 错误说明
1.如果分词报错，就把那个特殊字符切分重新改成原来的样子，然后再改成特殊分词的样子，这可能和缓存有关（需要改动jieba分词）
可以自己搜索jieba切分特殊字符
## 实验参数
217个句子

# 03similar
相似性实验

# ner_web_v1
将ner发布成服务
cd study/kg/some_example/ner/ner_web_v1
activate tensorflow-cpu
python manage.py runserver 127.0.0.1:8001










