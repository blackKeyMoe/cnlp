import math


class BM25:
    def __init__(self, docs):
        self.k1 = 2
        self.k2 = 1
        self.b = 0.75
        self.N = len(docs)
        self.AL = sum([len(doc) for doc in docs]) / self.N
        self.doctf = [{word: doc.count(word) for word in set(doc)}
                      for doc in docs]
        self.wordtf = dict()
        for doc in docs:
            for word in set(doc):
                self.wordtf[word] = self.wordtf.setdefault(word, 0) + 1

    def bm25(self, query, doc):
        query_words = {word: query.count(word) for word in set(query)}
        doc_words = {word: doc.count(word) for word in set(doc)}
        kvalue = (len(doc)*self.b + (1 - self.b)*self.AL) / self.AL
        score = 0
        for word in query_words.keys():
            score += doc_words.setdefault(word, 0) * (self.k1+1) / (kvalue + doc_words.setdefault(word, 0)) * \
                     query_words[word] * (self.k2+1) / (self.k2 + query_words[word]) * \
                     self._idf(word)
        return score

    def _tf(self, word, doc):
        dic = {word: doc.count(word) for word in set(doc)}
        return dic.setdefault(word, 0)

    def _idf(self, word):
        return math.log((self.N + 1)/ (self.wordtf[word]+1))


if __name__ == '__main__':
    bm25 = BM25([[u'文章', u'论文', u'游戏', u'图书馆'],
                 [u'游戏', u'团灭', u'首杀', u'反杀'],
                 [u'游戏', u'图书馆']])
    value = bm25.bm25([u'文章', u'游戏', u'图书馆'], [u'文章', u'论文', u'游戏'])