import re
import pickle

regx_chinese = re.compile(u"[\u4e00-\u9fa5]+")
regx_div = re.compile(u"[，。？！；：—]")

resdic = dict()

#
with open("icwb2-data/training/msr_training.utf8", encoding="utf-8") as file:
    last = ""
    for line in file.readlines():
        words = regx_chinese.findall(line)
        print(words)
        if not words:
            continue
        last, word = words[0][-1], words[0]
        i = 0
        while i+1 < len(word):
                resdic.setdefault(word[i], {})
                resdic[word[i]].setdefault(word[i+1], [0, 0])
                resdic[word[i]][word[i+1]][0] += 1
                # print(word[i], word[i+1], resdic[word[i]][word[i+1]])
                i += 1
        for word in words[1:]:
            i = 0
            resdic.setdefault(last, {})
            resdic[last].setdefault(word[0], [0, 0])
            resdic[last][word[0]][1] += 1
            # print(last, word[0], resdic[last][word[0]])
            last = word[-1]
            while i+1 < len(word):
                resdic.setdefault(word[i], {})
                resdic[word[i]].setdefault(word[i+1], [0, 0])
                resdic[word[i]][word[i+1]][0] += 1
                # print(word[i], word[i+1], resdic[word[i]][word[i+1]])
                i += 1
with open("res", "wb") as count:
    pickle.dump(resdic, count)
