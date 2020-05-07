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
             "B-Dtype": 1, "I-Dtype": 2,
             "B-Dmaterial": 3, "I-Dmaterial": 4,
             "B-DmaterialsStrength": 5, "I-DmaterialsStrength": 6,
             "B-Dshape": 7, "I-Dshape": 8,
             "B-Dcrh": 9, "I-Dcrh": 10,
             "B-Ddiameter": 11, "I-Ddiameter": 12,
             "B-Dlength": 13, "I-Dlength": 14,
             "B-Dweight": 15, "I-Dweight": 16,
             "B-Zspeed": 17, "I-Zspeed": 18,
             "B-Zangle": 19, "I-Zangle": 20,
             "B-Btype": 21, "I-Btype": 22,
             "B-Bthickness": 23, "I-Bthickness": 24,
             "B-Bstrength": 25, "I-Bstrength": 26,
             "B-Bdensity": 27, "I-Bdensity": 28,
             "B-Bratio": 29, "I-Bratio": 30,
             "B-Xdepth": 31, "I-Xdepth": 32,
             "B-Xpenetrate": 33, "I-Xpenetrate": 34,
             "B-F": 33, "I-F": 34
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
MAX_LEN = 100
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
model = load_model('model/ch_ner_model4.h5', custom_objects=custom_ob)
maxlen = 500
# sentence = "中华人民共和国国务院总理周恩来在外交部长陈毅的陪同下，连续访问了埃塞俄比亚等非洲10国以及阿尔巴尼亚。"
sentence = "弹体为新型缩比钻地弹，弹体材料为DT300高强度合金钢，" \
           "抗拉强度为1810MPa，内部装填物为高分子惰性材料，弹体直径25mm，" \
           "长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示。"
# sentence = "验采用Φ30mm口径射弹垂直侵彻，弹长138mm，弹径30mm，弹重0.5kg，选择适当的药量，可以获得需要的弹速，试验中射弹的着靶速度控制在276~456m/s范围内。"
s = ["为了分析某种结构助推钻地弹的侵彻效果，本文作者首先进行了无助推结构，即纯动能钻地弹侵彻试验，试验的基本状态为：弹丸质量为41.28kg，弹丸直径为125mm，要求弹丸着靶速度为560m/s，混凝土靶为C35 的圆柱形素混凝土靶，靶面直径2.4m，长4m，靶体密度为2360kg/m3。试验中弹丸实际着靶速度为563m/s，锥形弹坑深度为499mm，侵彻深度为1507mm。",
     "本文试验设计的助推钻地弹上的助推装置能够在弹丸侵彻过程中提供很大的推力，并推动弹丸短时间内做变加速运动。试验的基本状态为：弹丸质量为41.24kg，弹丸直径为125mm，要求弹丸着靶速度为560m/s，混凝土靶为C35的圆柱形素混凝土靶，靶面直径2.4m，长4m，靶体密度为2360kg/m3。试验中实际着靶速度为559m/s，锥形弹坑深度483mm，侵彻深度为1837mm。",
     "由于实验中只有一部分靶板被弹体贯穿，本文只研究靶板完全被贯穿的5个实验模型。其中Ａ 组：弹体以568.8，645.8，806.7m/s的速度侵彻素混凝土；Ｂ组：弹体以586.7，929.9m/s的速度侵彻钢纤维体积含量为3.0％的钢纤维混凝土。所有靶板均为直径500ｍｍ，高250ｍｍ 的圆柱体，外边界用钢板进行固结，弹体采用半球头脱壳尾翼稳定穿甲弹，长113ｍｍ，直径14.5ｍｍ，设计质量290ｇ．弹体垂直入射靶板．",
     "约260m/s速度下的打靶实验3发：第1发实验靶板倾角设计为400°，弹体撞靶速度为258m/s，弹体撞靶后未发生跳弹，侵入混凝土靶中；根据第１发实验结果，调整靶板倾角至33°，然后进行第2发打靶实验，弹体以254m/s的速度撞击靶板，由于钢筋的约束，弹体恰好嵌在靶板内部，根据弹道分析，弹体接近临界跳弹；然后继续调整靶板倾角至36°，又进行了第3发打靶实验，弹体在257m/s速度下撞击靶板，撞靶后弹体明显跳弹，弹体穿入防护钢靶中。"
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

        if tag=="Dtype":
            print("Dtype：","".join(word))
        if tag=="Dmaterial":
            print("".join(word))
        if tag=="DmaterialsStrength":
            print("".join(word))
        if tag=="Dshape":
            print("".join(word))
        if tag=="Dcrh":
            print("".join(word))
        if tag=="Ddiameter":
            print("".join(word))
        if tag=="Dlength":
            print("".join(word))
        if tag=="Dweight":
            print("".join(word))
        if tag=="Zspeed":
            print("".join(word))
        if tag=="Zangle":
            print("".join(word))
        if tag=="Btype":
            print("".join(word))
        if tag=="Bthickness":
            print("".join(word))
        if tag=="Bstrength":
            print("".join(word))
        if tag=="Bdensity":
            print("".join(word))
        if tag=="Bratio":
            print("".join(word))
        if tag=="Xdepth":
            print("".join(word))
        if tag=="Xpenetrate":
            print("".join(word))
        if tag=="F":
            print("".join(word))
    print(".................")




