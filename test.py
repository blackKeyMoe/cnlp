from sqlite3 import dbapi2 as sqlite
import pickle
import math
import re

pinyin = "a,ai,an,ang,ao,ba,bai,ban,bang,bao,bei,ben,beng,bi,bian,biao,bie,bin,bing,bo,bu,ca,cai,can," \
         "cang,cao,ce,cen,ceng,cha,chai,chan,chang,chao,che,chen,cheng,chi,chong,chou,chu,chua,chuai," \
         "chuan,chuang,chui,chun,chuo,ci,cong,cou,cu,cuan,cui,cun,cuo,da,dai,dan,dang,dao,de,dei,den," \
         "deng,di,dia,dian,diao,die,ding,diu,dong,dou,du,duan,dui,dun,duo,e,ei,en,eng,er,fa,fan,fang," \
         "fei,fen,feng,fiao,fo,fou,fu,ga,gai,gan,gang,gao,ge,gei,gen,geng,gong,gou,gu,gua,guai,guan," \
         "guang,gui,gun,guo,ha,hai,han,hang,hao,he,hei,hen,heng,hong,hou,hu,hua,huai,huan,huang,hui," \
         "hun,huo,ji,jia,jian,jiang,jiao,jie,jin,jing,jiong,jiu,ju,juan,jue,jun,ka,kai,kan,kang,kao," \
         "ke,kei,ken,keng,kong,kou,ku,kua,kuai,kuan,kuang,kui,kun,kuo,la,lai,lan,lang,lao,le,lei," \
         "leng,li,lia,lian,liang,liao,lie,lin,ling,liu,lo,long,lou,lu,luan,lue,lun,luo,lv,ma,mai,man," \
         "mang,mao,me,mei,men,meng,mi,mian,miao,mie,min,ming,miu,mo,mou,mu,na,nai,nan,nang,nao,ne," \
         "nei,nen,neng,ni,nian,niang,niao,nie,nin,ning,niu,nong,nou,nu,nuan,nue,nun,nuo,nv,o,ou,pa," \
         "pai,pan,pang,pao,pei,pen,peng,pi,pian,piao,pie,pin,ping,po,pou,pu,qi,qia,qian,qiang,qiao," \
         "qie,qin,qing,qiong,qiu,qu,quan,que,qun,ran,rang,rao,re,ren,reng,ri,rong,rou,ru,rua,ruan," \
         "rui,run,ruo,sa,sai,san,sang,sao,se,sen,seng,sha,shai,shan,shang,shao,she,shei,shen,sheng," \
         "shi,shou,shu,shua,shuai,shuan,shuang,shui,shun,shuo,si,song,sou,su,suan,sui,sun,suo,ta,tai," \
         "tan,tang,tao,te,tei,teng,ti,tian,tiao,tie,ting,tong,tou,tu,tuan,tui,tun,tuo,wa,wai,wan," \
         "wang,wei,wen,weng,wo,wu,xi,xia,xian,xiang,xiao,xie,xin,xing,xiong,xiu,xu,xuan,xue,xun,ya," \
         "yan,yang,yao,ye,yi,yin,ying,yo,yong,you,yu,yuan,yue,yun,za,zai,zan,zang,zao,ze,zei,zen," \
         "zeng,zha,zhai,zhan,zhang,zhao,zhe,zhei,zhen,zheng,zhi,zhong,zhou,zhu,zhua,zhuai,zhuan," \
         "zhuang,zhui,zhun,zhuo,zi,zong,zou,zu,zuan,zui,zun,zuo"
h = ['a', 'ai', 'an', 'ang', 'ao', 'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi',
     'bian', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu', 'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen',
     'ceng', 'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou',
     'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo', 'ci', 'cong', 'cou', 'cu',
     'cuan', 'cui', 'cun', 'cuo', 'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng', 'di',
     'dia', 'dian', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo',
     'e', 'ei', 'en', 'eng', 'er', 'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fiao', 'fo', 'fou', 'fu',
     'ga', 'gai', 'gan', 'gang', 'gao', 'ge', 'gei', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai',
     'guan', 'guang', 'gui', 'gun', 'guo', 'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng',
     'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo', 'ji', 'jia', 'jian',
     'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun', 'ka', 'kai',
     'kan', 'kang', 'kao', 'ke', 'kei', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan',
     'kuang', 'kui', 'kun', 'kuo', 'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lia',
     'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'lo', 'long', 'lou', 'lu', 'luan', 'lue',
     'lun', 'luo', 'lv', 'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng', 'mi', 'mian',
     'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu', 'na', 'nai', 'nan', 'nang', 'nao', 'ne',
     'nei', 'nen', 'neng', 'ni', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu', 'nong', 'nou',
     'nu', 'nuan', 'nue', 'nun', 'nuo', 'nv', 'o', 'ou', 'pa', 'pai', 'pan', 'pang', 'pao', 'pei',
     'pen', 'peng', 'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu', 'qi', 'qia', 'qian',
     'qiang', 'qiao', 'qie', 'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun', 'ran', 'rang',
     'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou', 'ru', 'rua', 'ruan', 'rui', 'run', 'ruo', 'sa',
     'sai', 'san', 'sang', 'sao', 'se', 'sen', 'seng', 'sha', 'shai', 'shan', 'shang', 'shao', 'she',
     'shei', 'shen', 'sheng', 'shi', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun',
     'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo', 'ta', 'tai', 'tan', 'tang', 'tao',
     'te', 'tei', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu', 'tuan', 'tui',
     'tun', 'tuo', 'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu', 'xi', 'xia', 'xian',
     'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun', 'ya', 'yan',
     'yang', 'yao', 'ye', 'yi', 'yin', 'ying', 'yo', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun', 'za',
     'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng', 'zha', 'zhai', 'zhan', 'zhang', 'zhao',
     'zhe', 'zhei', 'zhen', 'zheng', 'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang',
     'zhui', 'zhun', 'zhuo', 'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo']


# reg = re.compile("[\u4E00-\u9FA5]+")
# hhdic = {first: {last: 0 for last in h}
#          for first in h}
# with open("pku_test.utf8", encoding="utf-8") as file:
#     with open("hhdic", "wb") as wf:
#         for i in range(1000):
#             res = []
#             for item in reg.findall(file.readline()):
#                 sn = SnowNLP(item)
#                 res.append(sn.pinyin)
#             try:
#                 for sen in res:
#                     for index in range(len(sen)-1):
#                         hhdic[sen[index]][sen[index+1]] += 1
#             except KeyError as e:
#                 print(e, end="$ --> ")
#                 print(str(sen))
#         pickle.dump(hhdic, wf)
# conn = sqlite.connect("model.db")
# conn.execute("create table if not exists oh(observation,{0})".format(pinyin))
# conn.execute("create table if not exists hh(state,{0})".format(pinyin))
# with open("model/adic", "rb") as f:
#     dic = pickle.load(f)
#     for k, v in dic.items():
#         second = []
#         count = []
#         for sk, sv in v.items():
#             second.append(sk)
#             count.append(str(sv / (1+sum(v.values()))))
#         conn.execute("insert into oh(observation,{0}) values('{1}',{2})".format(",".join(second), k, ",".join(count)))
#     conn.commit()
# c = 0
# for item in conn.execute("select * from oh").fetchall():
#     print(c, end=" --> ")
#     print(str(item))
#     c += 1

# oh = {"指": {"B": 0.75, "M": 0.10, "E": 0.05, "S": 0.35},
#       "挥": {"B": 0.05, "M": 0.75, "E": 0.15, "S": 0.35},
#       "官": {"B": 0.20, "M": 0.15, "E": 0.80, "S": 0.30}}
# hh = {"B": {"B": 0.01, "M": 0.49, "E": 0.49, "S": 0.01},
#       "M": {"B": 0.01, "M": 0.21, "E": 0.47, "S": 0.31},
#       "E": {"B": 0.78, "M": 0.01, "E": 0.01, "S": 0.20},
#       "S": {"B": 0.20, "M": 0.29, "E": 0.03, "S": 0.48},}
# start = [0.7, 0.1, 0.1, 0.1]
# with open("tokenizertest", "wb") as model:
#     pickle.dump((oh, hh, start), model)


def character_tagging(input_file, output_file):
    input_data = open(input_file, 'r', encoding='utf-8')
    output_data = open(output_file, 'wb')
    train_data = {}
    hidden_data = {"S": {"S": 1, "B": 1, "M": 1, "E": 1},
                   "B": {"S": 1, "B": 1, "M": 1, "E": 1},
                   "M": {"S": 1, "B": 1, "M": 1, "E": 1},
                   "E": {"S": 1, "B": 1, "M": 1, "E": 1}}
    total = {"S": 0, "B": 0, "M": 0, "E": 0}
    hiddenlist = []

    def inner_train(inner, outter):
        train_data.setdefault(outter, {})
        train_data[outter].setdefault(inner, 0)
        train_data[outter][inner] += 1
        total[inner] += 1
        hiddenlist.append(inner)

    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                inner_train("S", word)
            else:
                inner_train("B", word[0])
                for w in word[1:len(word) - 1]:
                    inner_train("M", w)
                inner_train("E", word[-1])
    for sd in train_data.values():
        try:
            sd = {k: sd[k] / total[k] for k in total.keys()}
        except KeyError as e:
            sd.setdefault(e.args[0], 1 / total[e.args[0]])
    curr = hiddenlist[0]
    for h in hiddenlist[1:-1]:
        hidden_data[curr][h] += 1
        curr = h
    hidden_data = {k: {ik: hidden_data[k][ik] / sum(hidden_data[k].values()) for ik in hidden_data[k].keys()}
                   for k in hidden_data.keys()}
    start = [total[k] / sum(total.values()) for k in total.keys()]

    input_data.close()
    pickle.dump((train_data, hidden_data, start), output_data)
    output_data.close()


if __name__ == "__main__":
    character_tagging("pku_training.utf8", "pku_4_data")
    with open("pku_4_data", "rb") as f:
        dic = pickle.load(f)
