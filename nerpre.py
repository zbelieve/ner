import numpy as np
import keras
from keras.models import Sequential
from keras.models import Model
from keras.layers import Masking, Embedding, Bidirectional, LSTM, Dense, Input, TimeDistributed, Activation
from keras.preprocessing import sequence
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras import backend as K
char_vocab_path = "data/char_vocabs.txt" # 字典文件
train_data_path = "data/train_data.txt" # 训练数据
test_data_path = "data/test_data.txt" # 测试数据

special_words = ['<PAD>', '<UNK>'] # 特殊词表示

# "BIO"标记的标签
label2idx = {"O": 0,
             "B-Dname": 1, "I-Dname": 2,
             "B-Dmaterial": 3, "I-Dmaterial": 4,
             "B-Dweight": 5, "I-Dweight": 6,
             "B-Ddiameter": 7, "I-Ddiameter": 8,
             "B-Dlength": 9, "I-Dlength": 10,
             "B-Dspeed": 11, "I-Dspeed": 12,
             "B-Btype": 13, "I-Btype": 14,
             "B-Bdensity": 15, "I-Bdensity": 16,
             "B-F": 17, "I-F": 18,
             "B-Height": 19, "I-Height": 20,
             }
# 索引和BIO标签对应
idx2label = {idx: label for label, idx in label2idx.items()}
# 读取字符词典文件
with open(char_vocab_path, "r", encoding="utf8") as fo:
    char_vocabs = [line.strip() for line in fo]
char_vocabs = special_words + char_vocabs

# 字符和索引编号对应
idx2vocab = {idx: char for idx, char in enumerate(char_vocabs)}
vocab2idx = {char: idx for idx, char in idx2vocab.items()}

EPOCHS = 1
BATCH_SIZE = 50
EMBED_DIM = 1
HIDDEN_SIZE = 1
MAX_LEN = 10
VOCAB_SIZE = len(vocab2idx)
CLASS_NUMS = len(label2idx)
## BiLSTM+CRF模型构建
inputs = Input(shape=(MAX_LEN,), dtype='int32')
x = Masking(mask_value=0)(inputs)
x = Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(x)
x = Bidirectional(LSTM(HIDDEN_SIZE, return_sequences=True))(x)
x = TimeDistributed(Dense(CLASS_NUMS))(x)
outputs = CRF(CLASS_NUMS)(x)
model = Model(inputs=inputs, outputs=outputs)
model.summary()

def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.
        Only computes a batch-wise average of recall.
        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.
        Only computes a batch-wise average of precision.
        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


'''用来预测'''

from keras.models import load_model
import numpy as np
custom_ob = {'CRF': CRF,"crf_loss":crf_loss,"crf_viterbi_accuracy":crf_viterbi_accuracy,"f1":f1}
model = load_model('model/ch_ner_model2.h5', custom_objects=custom_ob)
maxlen = 200
# sentence = "中华人民共和国国务院总理周恩来在外交部长陈毅的陪同下，连续访问了埃塞俄比亚等非洲10国以及阿尔巴尼亚。"
sentence = "弹体为新型缩比钻地弹，弹体材料为DT300高强度合金钢，" \
           "抗拉强度为1810MPa，内部装填物为高分子惰性材料，弹体直径25mm，" \
           "长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示。"
# sentence = "验采用Φ30mm口径射弹垂直侵彻，弹长138mm，弹径30mm，弹重0.5kg，选择适当的药量，可以获得需要的弹速，试验中射弹的着靶速度控制在276~456m/s范围内。"
s = ["弹体为新型缩比钻地弹，弹体材料为DT300高强度合金钢,抗拉强度为1810MPa，内部装填物为高分子惰性材料，弹体直径25mm。",
     "试验弹体直径为10mm，质量约为50g",
     "设计了一款Φ1000mm的试验弹丸",
     "混凝土靶直径为100m"
    ]
for i in s:
    sent_chars = list(i)
    sent2id = [vocab2idx[word] if word in vocab2idx else vocab2idx['<UNK>'] for word in sent_chars]
    sent2id_new = np.array([[0] * (maxlen - len(sent2id)) + sent2id[:maxlen]])
    y_pred = model.predict(sent2id_new)
    y_label = np.argmax(y_pred, axis=2)
    y_label = y_label.reshape(1, -1)[0]
    y_ner = [idx2label[i] for i in y_label][-len(sent_chars):]

    # print(idx2label)
    print(sent_chars)
    # print(sent2id)
    # print(y_ner)


    # 对预测结果进行命名实体解析和提取
    def get_valid_nertag(input_data, result_tags):
        result_words = []
        start, end = 0, 1  # 实体开始结束位置标识
        tag_label = "O"  # 实体类型标识
        for i, tag in enumerate(result_tags):
            if tag.startswith("B"):
                if tag_label != "O":  # 当前实体tag之前有其他实体
                    result_words.append((input_data[start: end], tag_label))  # 获取实体
                tag_label = tag.split("-")[1]  # 获取当前实体类型
                start, end = i, i + 1  # 开始和结束位置变更
            elif tag.startswith("I"):
                temp_label = tag.split("-")[1]
                if temp_label == tag_label:  # 当前实体tag是之前实体的一部分
                    end += 1  # 结束位置end扩展
            elif tag == "O":
                if tag_label != "O":  # 当前位置非实体 但是之前有实体
                    result_words.append((input_data[start: end], tag_label))  # 获取实体
                    tag_label = "O"  # 实体类型置"O"
                start, end = i, i + 1  # 开始和结束位置变更
        if tag_label != "O":  # 最后结尾还有实体
            result_words.append((input_data[start: end], tag_label))  # 获取结尾的实体
        return result_words


    result_words = get_valid_nertag(sent_chars, y_ner)
    for (word, tag) in result_words:
        if tag=="Ddiameter":
            print("弹体直径：","".join(word))

    print(".................")




