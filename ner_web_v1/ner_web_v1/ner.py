from django.http import HttpResponse


def hello(request):
    id = request.GET.get('id', '0')
    print(id)
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
    import argparse
    import pymysql
    import codecs
    import json
    char_vocab_path = "E:/study/kg/some_example/ner/ner_web_v1/static/data/char_vocabs.txt"  # 字典文件
    train_data_path = "./static/data/train_data.txt"  # 训练数据
    test_data_path = "./static/data/test_data.txt"  # 测试数据
    # 设置参数
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--url", required=True,help="path to the text url")
    # args = vars(ap.parse_args())
    # TextUrl = args['url']
    # with open(TextUrl,"r",encoding='utf-8') as f:
    #     str = f.read()
    # print(str)
    # s=[]
    # s.append(str)

    '''数据库连接'''
    # 根据流程
    # 1.我们先建立数据库的连接信息
    host = "127.0.0.1"
    user = "root"
    password = "root"
    port = 3306
    mysql = pymysql.connect(host=host, user=user, password=password, port=port)
    # 2.新建个查询页面
    cursor = mysql.cursor()
    # 3编写sql
    sql = 'SELECT TM_TEXT FROM tm.tm_info WHERE TM_ID = ' + id
    # 4.执行sql
    cursor.execute(sql)
    # 5.查看结果
    # result = cursor.fetchone() #用于返回单条数据
    results = cursor.fetchall()  # 用于返回多条数据
    TM_TEXT = results[0][0]
    # print(TM_TEXT)
    s = []
    s.append(TM_TEXT)
    # 6.关闭查询
    cursor.close()
    # 关闭数据库
    mysql.close()

    special_words = ['<PAD>', '<UNK>']  # 特殊词表示

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
    custom_ob = {'CRF': CRF, "crf_loss": crf_loss, "crf_viterbi_accuracy": crf_viterbi_accuracy, "f1": f1}
    keras.backend.clear_session()
    model = load_model('E:/study/kg/some_example/ner/01bilstm-ner/model/ch_ner_model4.h5', custom_objects=custom_ob)
    maxlen = 500
    # sentence = "中华人民共和国国务院总理周恩来在外交部长陈毅的陪同下，连续访问了埃塞俄比亚等非洲10国以及阿尔巴尼亚。"
    # sentence = "弹体为新型缩比钻地弹，弹体材料为DT300高强度合金钢，" \
    #            "抗拉强度为1810MPa，内部装填物为高分子惰性材料，弹体直径25mm，" \
    #            "长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示。"
    # sentence = "验采用Φ30mm口径射弹垂直侵彻，弹长138mm，弹径30mm，弹重0.5kg，选择适当的药量，可以获得需要的弹速，试验中射弹的着靶速度控制在276~456m/s范围内。"
    # s = ["弹体为新型缩比钻地弹，弹体材料为DT300高强度合金钢,抗拉强度为1810MPa，内部装填物为高分子惰性材料，弹体直径25mm。长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示。混凝土靶直径为100m，长径比为6。在本次的实验中混凝土靶标的长度为200cm.",
    #      "试验弹体直径为10mm，质量约为50g，长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示。混凝土靶直径为100m，长径比为6。在本次的实验中混凝土靶标的长度为200cm.",
    #      "设计了一款Φ1000mm的试验弹丸，长径比为6，弹壳壁厚与弹径比为0.15，弹体质量约340g，如图2所示，混凝土靶直径为100m，长径比为6。在本次的实验中混凝土靶标的长度为200cm.",
    #      "混凝土靶直径为100m，长径比为6。在本次的实验中混凝土靶标的质量为100kg."
    #     ]
    for i in s:
        sent_chars = list(i)
        sent2id = [vocab2idx[word] if word in vocab2idx else vocab2idx['<UNK>'] for word in sent_chars]
        sent2id_new = np.array([[0] * (maxlen - len(sent2id)) + sent2id[:maxlen]])
        y_pred = model.predict(sent2id_new)
        y_label = np.argmax(y_pred, axis=2)
        y_label = y_label.reshape(1, -1)[0]
        y_ner = [idx2label[i] for i in y_label][-len(sent_chars):]

        # print(idx2label)
        # print(sent_chars)
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

    Ddiameter = []
    result_words = get_valid_nertag(sent_chars, y_ner)
    Dtype = []
    Dmaterial = []
    DmaterialsStrength = []
    Dshape = []
    Dcrh = []
    Ddiameter = []
    Dlength = []
    Dweight = []
    Zspeed = []
    Zangle = []
    Btype = []
    Bthickness = []
    Bstrength = []
    Bdensity = []
    Bratio = []
    Xdepth = []
    Xpenetrate = []
    F = []

    TextLine = []
    for (word, tag) in result_words:
        # 一条数据

        if tag == "Dtype":
            # print("Dtype：", "".join(word))
            Dtype.append("".join(word))
        if tag == "Dmaterial":
            # print("Dmaterial：","".join(word))
            Dmaterial.append("".join(word))
        if tag == "DmaterialsStrength":
            # print("DmaterialsStrength：","".join(word))
            DmaterialsStrength.append("".join(word))
        if tag == "Dshape":
            # print("Dshape：","".join(word))
            Dshape.append("".join(word))
        if tag == "Dcrh":
            # print("Dcrh：","".join(word))
            Dcrh.append("".join(word))
        if tag == "Ddiameter":
            # print("Ddiameter：","".join(word))
            Ddiameter.append(word)
        if tag == "Dlength":
            # print("Dlength：","".join(word))
            Dlength.append("".join(word))
        if tag == "Dweight":
            # print("Dweight：","".join(word))
            Dweight.append("".join(word))
        if tag == "Zspeed":
            # print("Zspeed：","".join(word))
            Zspeed.append("".join(word))
        if tag == "Zangle":
            # print("Zangle：","".join(word))
            Zangle.append("".join(word))
        if tag == "Btype":
            # print("Btype：","".join(word))
            Btype.append("".join(word))
        if tag == "Bthickness":
            # print("Bthickness：","".join(word))
            Bthickness.append("".join(word))
        if tag == "Bstrength":
            # print("Bstrength：","".join(word))
            Bstrength.append("".join(word))
        if tag == "Bdensity":
            # print("Bdensity：","".join(word))
            Bdensity.append("".join(word))
        if tag == "Bratio":
            # print("Bratio：","".join(word))
            Bratio.append("".join(word))
        if tag == "Xdepth":
            # print("Xdepth：","".join(word))
            Xdepth.append("".join(word))
        if tag == "Xpenetrate":
            # print("Xpenetrate：","".join(word))
            Xpenetrate.append("".join(word))
        if tag == "F":
            # print("F：","".join(word))
            F.append("".join(word))
    TextLine = {
        '靶标类型': Dtype,
        '弹体材料': Dmaterial,
        '弹体材料强度': DmaterialsStrength,
        '弹头形状': Dshape,
        'CRH ': Dcrh,
        '弹体直径': Ddiameter,
        '弹体长度': Dlength,
        '弹体质量': Dweight,
        '着靶速度': Zspeed,
        '命中角': Zangle,
        '靶标材料种类': Btype,
        '靶标厚度': Bthickness,
        '靶标抗压强度': Bstrength,
        '靶标材料密度': Bdensity,
        '靶标配筋率': Bratio,
        '侵彻深度': Xdepth,
        '贯穿': Xpenetrate,
        '发射炮类型': F
    }

    # length=[len(Dtype),len(Dmaterial),len(DmaterialsStrength),len(Dshape),len(Dcrh),len(Ddiameter),len(Dlength),
    #         len(Dweight),len(Zspeed),len(Zangle),len(Btype),len(Bthickness),len(Bstrength),len(Bdensity),
    #         len(Bdensity),len(Bratio),len(Xdepth),len(Xpenetrate),len(F)]
    #
    # length.sort(reverse=True)
    # lastLength = length[0]
    # dataAll = []
    #
    # for i in range(0,lastLength):
    #     data={
    #         "靶标类型": "",
    #         "弹体材料": "",
    #         "弹体材料强度": "",
    #         "弹头形状": "",
    #         " CRH ": "",
    #         "弹体直径": "",
    #         "弹体长度": "",
    #         "弹体质量": "",
    #         "着靶速度": "",
    #         "命中角": "",
    #         "靶标材料种类": "",
    #         "靶标厚度": "",
    #         "靶标抗压强度": "",
    #         "靶标材料密度": "",
    #         "靶标配筋率": "",
    #         "侵彻深度": "",
    #         "贯穿": "",
    #         "发射炮类型": ""
    #     }
    #     if len(Dtype)==1:
    #         data["靶标类型"] = Dtype[0]
    #     elif len(Dtype)>1:
    #         data["靶标类型"] = Dtype[i]
    #     if len(Zspeed)==1:
    #         data["着靶速度"] = Zspeed[0]
    #     elif len(Zspeed)>1:
    #         data["着靶速度"] = Zspeed[i]
    #     if len(Zangle)==1:
    #         data["命中角"] = Zangle[0]
    #     elif len(Zangle)>1:
    #         data["命中角"] = Zangle[i]
    #     dataAll.append(data)

    # print(".................")
    # print(Zspeed)
    # print(Zangle)
    return HttpResponse(json.dumps(TextLine,ensure_ascii=False), content_type="application/json,charset=utf-8")

