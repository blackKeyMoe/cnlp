from sqlite3 import dbapi2 as sqlite
from snownlp import SnowNLP


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
pin = pinyin.split(",")


class Hmm:
    def __init__(self, name):
        self.h = []
        self.lenh = 0
        self.o = []
        self.oh = dict()
        self.hh = dict()
        self.start = []
        self.doc = []
        self.conn = sqlite.connect(name)

    def setmodel(self, state, observation):
        self.h = state
        self.lenh = len(self.h)
        self.o = observation
        self.start = [1 / len(self.h) for i in self.h]
        for ob in observation:
            self.oh.setdefault(ob, {})
            for s in state:
                value = self.conn.execute("select {0} from oh where observation='{1}'".format(s, ob)).fetchone()[0]
                self.oh[ob].setdefault(s, value if value is not None else 0.0)
        for first in state:
            value = self.conn.execute("select * from hh where state='{0}'".format(first)).fetchall()[0][1:]
            self.hh.setdefault(first, {k: v for k, v in zip(pin, value)})
        print("load model successfully")

    def hmm(self, doc):
        pass

    # 前向算法
    # 浮点数运算精度不足，需要调整，下同
    def forward(self):
        alph = []
        start = [st*ho for st, ho in zip(self.start, self.oh[self.o[0]].values())]
        alph.append(start)
        for i in range(1, len(self.o)):
            temp = [sum([alph[i-1][index]*self.hh[self.h[index]][self.h[i-1]] for index in range(self.lenh)]) * ho
                    for ho in self.oh[self.o[i]].values()]
            alph.append(temp)
        return sum(alph[-1])

    # 后向算法
    def backward(self):
        beta = [[] for i in range(len(self.o))]
        end = [1 for i in range(self.lenh)]
        beta[-1] = end
        for i in range(1, len(self.o)):
            beta[-i-1] = [sum([self.hh[qi][self.h[j]] * self.oh[self.o[-i]][self.h[j]] * beta[-i][j]
                               for j in range(self.lenh)])
                          for qi in self.h]
        return sum([self.start[i] * self.oh[self.o[0]][self.h[i]] * beta[0][i]
                    for i in range(self.lenh)])

    # 维特比算法
    def viterbi(self):
        delt = [[self.start[i]*self.oh[self.o[0]][self.h[i]]
                for i in range(self.lenh)]]
        phi = [[0 for i in range(self.lenh)]]
        for t in range(1, len(self.o)):
            dt, pt = [], []
            for i in range(self.lenh):
                p = [delt[t-1][j]*self.hh[self.h[j]][self.h[i]] for j in range(self.lenh)]
                m = max(p)
                pt.append(self.h[p.index(m)])
                dt.append(m * self.oh[self.o[t]][self.h[i]])
            delt.append(dt)
            phi.append(pt)
        mp = delt[-1].index(max(delt[-1]))
        dequence = [self.h[mp]]
        for i in range(len(self.o)-1):
            mp = self.h.index(phi[-i-1][mp])
            dequence.insert(0, self.h[mp])
        return dequence

if __name__ == "__main__":
    hmms = Hmm("model.db")

    # hmms.h = ['1', '2', '3']
    # hmms.lenh = len(hmms.h)
    # hmms.o = ['r', 'w', 'r']
    # hmms.hh = {'1': {'1': 0.5, '2': 0.2, '3': 0.3},
    #            '2': {'1': 0.3, '2': 0.5, '3': 0.2},
    #            '3': {'1': 0.2, '2': 0.3, '3': 0.5}}
    # hmms.oh = {'r': {'1': 0.5, '2': 0.4, '3': 0.7},
    #            'w': {'1': 0.5, '2': 0.6, '3': 0.3}}
    # hmms.start = [0.2, 0.4, 0.4]

    # hmms.setmodel(pin, ["市", "长"])
    # print(hmms.forward())
    # print(hmms.backward())
    # print(hmms.viterbi())
