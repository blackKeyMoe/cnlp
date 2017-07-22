import pickle
import Crypto

with open("res", "rb") as file:
    countdic = pickle.load(file)
print("来看一组有趣的数据：")
print("方括号内的第一个数字表示在同一个词内部，这两个字相邻出现的次数")
print("第二个数字表示在两个不同的词之间，这两个字相邻出现的次数。相邻默认是有序的")
print("江", "泽", countdic["江"]["泽"])
print("泽", "民", countdic["泽"]["民"])
print("民", "主", countdic["民"]["主"])
print("主", "席", countdic["主"]["席"])
