# encoding: utf-8


class TextRank:
    def __init__(self, doc):
        self.d = 0.85
        self.window = 6
        self.doc = doc
        self.words = set(doc)
        self.weight = {start: {end: 0 for end in self.words}
                       for start in self.words}
        self.generate_graphic()
        self.weightsum = {word: sum([self.weight[word][end] for end in self.words if self.weight[word][end] is not 0])
                          for word in self.words}
        self.score = {word: 1 for word in self.words}

    def generate_graphic(self):
        for index in range(len(self.doc)):
            window_words = self.doc[index: index+self.window]
            for start in window_words:
                for end in window_words:
                    if start is not end:
                        self.weight[start][end] += 1

    def rank(self):
        for x in range(10):
            for word in self.words:
                word_sum = 0
                for end in self.words:
                    word_sum += self.weight[word][end] / self.weightsum[end] * self.score[end]
                self.score[word] = (1 - self.d) + self.d * word_sum

    def textrank(self, top=5):
        self.rank()
        scorel = list(self.score.items())
        return sorted(scorel, key=lambda x: x[1], reverse=True)[:top]

if __name__ == '__main__':
    text = ['搜索', '结果', '排序', '搜索', '引擎', '核心', '部分', '程度', '决定', '搜索', '引擎', '质量', '好坏',
            '用户', '满意度', '实际', '搜索', '结果', '排序', '因子', '因素', '用户', '查询', '网页', '内容',
            '相关', '以及', '网页', '链接', '情况', '这里', '总结', '网页', '内容', '用户', '查询', '相关', '内容']
    tr = TextRank(text)
    for w in range(2, 7):
        tr.window = w
        print(tr.textrank(3))
