from sqlite3 import dbapi2 as sqlite
import pickle
import re


class Hmm:
    def __init__(self, name="segmodel"):
        with open(name, "rb") as model:
            self.oh, self.hh, self.start = pickle.load(model)
        self.h = ["B", "M", "E", "S"]
        self.doc = []
        self.lenh = len(self.h)
        self.result = []

    def sentence(self, doc):
        regc = re.compile(r"[\u4e00-\u9fa5]")
        regx = re.compile(r"[\u4e00-\u9fa5]+|[\W+]|[a-zA-Z]+|\d+")
        self.doc = regx.findall(doc)
        tmp = ""
        for s in self.doc:
            if "\u4e00" <= s[0] <= "\u9fa5":
                for i, item in enumerate(self.viterbi(s)):
                    print(item)
                    if item == "B":
                        tmp += s[i]
                    elif item == "M":
                        tmp += s[i]
                    elif item == "E":
                        tmp += s[i]
                        self.result.append(tmp)
                        tmp = ""
                    elif item == "S":
                        tmp = s[i]
                        self.result.append(tmp)
                        tmp = ""
                    else:
                        print("ERROR: tokenizer has been destroyed by atm")
            else:
                if tmp is not "":
                    self.result.append(tmp)
                    tmp = ""
                self.result.append(s)
        print(self.result)

    def hmm(self, doc):
        pass

    # 前向算法
    # 浮点数运算精度不足，需要调整，下同
    def forward(self):
        alph = []
        start = [st*ho for st, ho in zip(self.start, self.oh[self.doc[0]].values())]
        alph.append(start)
        for i in range(1, len(self.doc)):
            temp = [sum([alph[i-1][index]*self.hh[self.h[index]][self.h[i-1]] for index in range(self.lenh)]) * ho
                    for ho in self.oh[self.doc[i]].values()]
            alph.append(temp)
        return sum(alph[-1])

    # 后向算法
    def backward(self):
        beta = [[] for i in range(len(self.doc))]
        end = [1 for i in range(self.lenh)]
        beta[-1] = end
        for i in range(1, len(self.doc)):
            beta[-i-1] = [sum([self.hh[qi][self.h[j]] * self.oh[self.doc[-i]][self.h[j]] * beta[-i][j]
                               for j in range(self.lenh)])
                          for qi in self.h]
        return sum([self.start[i] * self.oh[self.doc[0]][self.h[i]] * beta[0][i]
                    for i in range(self.lenh)])

    # 维特比算法
    def viterbi(self, observertion):
        delt = [[self.start[i]*self.oh[observertion[0]][self.h[i]]
                for i in range(self.lenh)]]
        phi = [[0 for i in range(self.lenh)]]
        for t in range(1, len(observertion)):
            dt, pt = [], []
            for i in range(self.lenh):
                p = [delt[t-1][j]*self.hh[self.h[j]][self.h[i]] for j in range(self.lenh)]
                m = max(p)
                pt.append(self.h[p.index(m)])
                dt.append(m * self.oh[observertion[t]][self.h[i]])
            delt.append(dt)
            phi.append(pt)
        mp = delt[-1].index(max(delt[-1]))
        dequence = [self.h[mp]]
        for i in range(len(observertion)-1):
            mp = self.h.index(phi[-i-1][mp])
            dequence.insert(0, self.h[mp])
        return dequence

if __name__ == "__main__":
    # hmms = Hmm("model.db")

    # hmms.h = ['1', '2', '3']
    # hmms.lenh = len(hmms.h)
    # hmms.o = ['r', 'w', 'r']
    # hmms.hh = {'1': {'1': 0.5, '2': 0.2, '3': 0.3},
    #            '2': {'1': 0.3, '2': 0.5, '3': 0.2},
    #            '3': {'1': 0.2, '2': 0.3, '3': 0.5}}
    # hmms.oh = {'r': {'1': 0.5, '2': 0.4, '3': 0.7},
    #            'w': {'1': 0.5, '2': 0.6, '3': 0.3}}
    # hmms.start = [0.2, 0.4, 0.4]

    # hmms.setmodel(pin, ["北", "京", "市", "长"])
    # print(hmms.forward())
    # print(hmms.backward())
    # print(hmms.viterbi())
    hmms = Hmm("pku_4_data")
    hmms.sentence("迫击炮炮击金门")
