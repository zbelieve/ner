char_vocab_path = "data/char_vocabs.txt" # 字典文件
train_data_path = "data/train_data.txt" # 训练数据
test_data_path = "data/train_data.txt" # 测试数据

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
print(len(idx2vocab))
vocab2idx = {char: idx for idx, char in idx2vocab.items()}
print(len(vocab2idx))
# 读取训练语料
def read_corpus(corpus_path, vocab2idx, label2idx):
    datas, labels = [], []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_ = [], []
    for line in lines:
        if line != '\n':
            # [char, label] = line.strip().split()
            c = line.split("\t")
            char = c[0]
            label = c[1].split("\n")[0]
            sent_.append(char)
            tag_.append(label)
        else:
            sent_ids = [vocab2idx[char] if char in vocab2idx else vocab2idx['<UNK>'] for char in sent_]
            tag_ids = [label2idx[label] if label in label2idx else 0 for label in tag_]
            datas.append(sent_ids)
            labels.append(tag_ids)
            sent_, tag_ = [], []
    return datas, labels

# 加载训练集
train_datas, train_labels = read_corpus(train_data_path, vocab2idx, label2idx)
train_datas, train_labels = train_datas,train_labels
# 加载测试集
test_datas, test_labels = read_corpus(test_data_path, vocab2idx, label2idx)
test_datas, test_labels = test_datas, test_labels

# print(train_datas[5])
# print()
# print([idx2vocab[idx] for idx in train_datas[5]])
# print()
# print(train_labels[5])
# print()
# print([idx2label[idx] for idx in train_labels[5]])

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
K.clear_session()

EPOCHS = 3000
BATCH_SIZE = 2
EMBED_DIM = 1
HIDDEN_SIZE = 1
MAX_LEN = 200
VOCAB_SIZE = len(vocab2idx)
CLASS_NUMS = len(label2idx)
print(VOCAB_SIZE,CLASS_NUMS)

print('padding sequences')
train_datas = sequence.pad_sequences(train_datas, maxlen=MAX_LEN)
train_labels = sequence.pad_sequences(train_labels, maxlen=MAX_LEN)
test_datas = sequence.pad_sequences(test_datas, maxlen=MAX_LEN)
test_labels = sequence.pad_sequences(test_labels, maxlen=MAX_LEN)
print('x_train shape:', train_datas.shape)
print('x_test shape:', test_datas.shape)

train_labels = keras.utils.to_categorical(train_labels, CLASS_NUMS)
test_labels = keras.utils.to_categorical(test_labels, CLASS_NUMS)
print('trainlabels shape:', train_labels.shape)
print('testlabels shape:', test_labels.shape)

## BiLSTM+CRF模型构建
inputs = Input(shape=(MAX_LEN,), dtype='int32')
x = Masking(mask_value=0)(inputs)
x = Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(x)
x = Bidirectional(LSTM(HIDDEN_SIZE, return_sequences=True))(x)
x = TimeDistributed(Dense(CLASS_NUMS))(x)
outputs = CRF(CLASS_NUMS)(x)
model = Model(inputs=inputs, outputs=outputs)
model.summary()


import numpy as np
from keras.callbacks import Callback
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from keras.callbacks import Callback

from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


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




model.compile(loss=crf_loss, optimizer='adam', metrics=[crf_viterbi_accuracy,f1])
model.fit(train_datas, train_labels, epochs=EPOCHS, verbose=1, validation_split=0.1,validation_data=(test_datas,test_labels),shuffle=True)

score = model.evaluate(test_datas, test_labels, batch_size=BATCH_SIZE)
print(model.metrics_names)
print(score)

# save model
model.save("./model/ch_ner_model2.h5")


