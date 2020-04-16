with open("train_data.txt","r",encoding="utf-8") as f:
    with open("train_data.txt", encoding='utf-8') as fr:
        lines = fr.readlines()
    # print(lines)
    dict = []
    for line in lines:
        if line != '\n':
            char = line.split("\t")
            print(char[0])
            if char[0] not in dict:
                dict.append(char[0])

        with open("char_vocabs.txt",'w',encoding='utf-8') as fb:
            for d in dict:
                fb.write(d)
                fb.write("\n")