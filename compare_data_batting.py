from data_output import IDreturn_imp
from data_output import PlayerRecordBatting
from data_output import PlayerRecordPitching
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def compare_batting(what):
    n = int(input('Input the number of players you want to compare'))
    ply = []
    width = 0.3
    for i in range(n):
        print("You are now in the %i th player" %(i+1)) #数に関わらず全部thになるが仕方ない
        first = input('Input the first name of player you want to compare')
        last = input('Input the first name of player you want to compare')
        ply.append(PlayerRecordBatting(first, last, what))
        blist = np.array([width * i] * len(list(PlayerRecordBatting(first, last, what))))
        #widthを足して棒グラフを重ねないように表示、for文ループをこれ以上増やすとアレなのでnumpyを使う
        plt.bar(np.array(list(range(len(list(PlayerRecordBatting(first, last, what)))))+ blist), ply[i], width=width, label="%s" %(first + " " + last))
        #ついでに凡例名を名前に、地味に苦労したがこれが一番うまくいく

    # X軸の数字が必ず整数になるようにする
    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.legend()

def compare_batting_accumulation(what):
    n = int(input('Input the number of players you want to compare'))
    ply = []
    width = 0.3
    for i in range(n):
        print("You are now in the %i th player" %(i+1)) #数に関わらず全部thになるが仕方ない
        first = input('Input the first name of player you want to compare')
        last = input('Input the first name of player you want to compare')
        ply.append(np.cumsum(PlayerRecordBatting(first, last, what))) #numpyにおいてcumsumは累積和らしい。cumulative summaryかな
        blist = np.array([width * i] * len(list(PlayerRecordBatting(first, last, what))))
        #widthを足して棒グラフを重ねないように表示、for文ループをこれ以上増やすとアレなのでnumpyを使う
        plt.bar(np.array(list(range(len(list(PlayerRecordBatting(first, last, what)))))+ blist), ply[i], width=width, label="%s" %(first + " " + last))
    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.legend()

if __name__ == '__main__':
    answer = input('Do you want to see acumulated data? (y/n)')
    if (answer == 'y'):
        what = input('What kind of data do you want to refer?')
        compare_batting_accumulation(what)
        plt.show()
    if (answer == 'n'):
        what = input('What kind of data do you want to refer?')
        compare_batting(what)
        plt.show()
