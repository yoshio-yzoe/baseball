import pandas as pd
import sklearn


#wRCを計算するためにはその年のリーグ総得点数およびリーグ総打席数が必要
#yearIDからそれらを出す関数が必要
#そもそもリーグ総得点数およびリーグ総打席数のデータは何処
#Teams.csvに各チームの年度ごとのがあるのでまあ使えるかな
def Sum_R(year):
    import pandas as pd
    df_team = pd.read_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/Teams.csv")
    return sum(df_team[df_team["yearID"] == year].R)

def Sum_PA(year):
    import pandas as pd
    df_team = pd.read_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/Teams.csv")
    df_team = df_team.fillna(int(0))
    return int((sum(df_team[df_team["yearID"] == year].AB) + sum(df_team[df_team["yearID"] == year].BB) + sum(df_team[df_team["yearID"] == year].HBP) + sum(df_team[df_team["yearID"] == year].SF) + sum(df_team[df_team["yearID"] == year].SB)))

def database_batting():
    df_batting_origin = pd.read_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/Batting.csv")
    df_batting = df_batting_origin.copy()
    df_batting = df_batting.fillna(int(0)) #欠損を0に置き換え
    df_batting['AVG'] = df_batting['H']/df_batting['AB']
    #出塁率 ＝ （安打数＋四球＋死球）÷（打数＋四球＋死球＋犠飛）
    df_batting['OBP'] = (df_batting['H'] + df_batting['BB'] + df_batting['HBP']) / (df_batting['AB'] + df_batting['BB'] + df_batting['HBP'] + df_batting['SF'])
    #塁打数
    df_batting['TB'] = (df_batting['H'] - df_batting['2B'] - df_batting['3B'] - df_batting['HR']) * 1 + df_batting['2B'] * 2 + df_batting['3B'] * 3 + df_batting['HR'] * 4

    #長打率 ＝ 塁打数÷打数
    df_batting['SLG'] = df_batting['TB'] / df_batting['AB']

    df_batting['OPS'] = df_batting['OBP'] + df_batting['SLG']

    #wOBA (2012年MLB) = {0.691×(四球 - 敬遠) + 0.722×死球 + 0.884×単打 + 1.257×二塁打 + 1.593×三塁打 + 2.058×本塁打}÷(打数 + 四球 – 敬遠 + 犠飛 + 死球)
    df_batting['wOBA'] = (0.691 * (df_batting['BB'] - df_batting['IBB']) + 0.722 * df_batting['HBP'] + 0.884 * (df_batting['H'] - df_batting['2B'] - df_batting['3B'] - df_batting['HR']) + 1.257 * df_batting['2B'] +1.593 * df_batting['3B'] + 2.058 * df_batting['HR']) / (df_batting['AB'] + df_batting['BB'] - df_batting['IBB'] + df_batting['SF'] + df_batting['HBP'])
    df_batting['wRAA'] = (df_batting['AB'] + df_batting['BB'] + df_batting['HBP'] + df_batting['SF'] + df_batting['SH'])*(df_batting['wOBA'] - 0.320)/1.25

    return df_batting

def WRC():
    df_batting = database_batting()
    #wRC = wRAA + (リーグ総得点数 / リーグ総打席数) × 打席数
    df_batting['wRC'] = df_batting['wRAA'] + (df_batting['AB'] + df_batting['BB'] + df_batting['HBP'] + df_batting['SF'] + df_batting['SH']) * df_batting['yearID'].map(Sum_R) / df_batting['yearID'].map(Sum_PA)
    return df_batting

if __name__ == '__main__':
    df = WRC()
    df.to_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/BattingCopy.csv")
