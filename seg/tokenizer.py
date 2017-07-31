from src_of_everything.hmm import Hmm


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
    hmms.sentence("我爱北京天安门")
