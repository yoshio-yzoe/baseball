import pandas as pd
import numpy as np
import sys
from createSaborDatabase import database_batting

def IDreturn_imp(firstname, lastname):
    df_people = pd.read_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/People.csv")
    dflist = list(df_people.query('nameFirst == @firstname and nameLast == @lastname').playerID)
    if (dflist[0] == dflist[-1]):
        return dflist[0]
    else:
        print('There are people having same first and last names.')
        birth_year = int(input('Please input the Birth Year of the player you are trying to look up.'))
        dflist2 = list(df_people.query('nameFirst == @firstname and nameLast == @lastname and birthYear == @birth_year').playerID)
        if (dflist2[0] == dflist2[-1]):
            return dflist2[0]
        else:
            print('There are still people having same first and last names. Please input the Birth Month and Date of the player you are trying to look up')
            birth_month = int(input('Put the birth month.'))
            birth_day = int(input('Put the birth day.'))
            dflist3 = list(df_people.query('nameFirst == @firstname and nameLast == @lastname and birthYear == @birth_year and birthMonth == @birth_month and birthDay == @birth_day').playerID)
            return dflist3[0]

def PlayerRecordBatting(firstname, lastname, what):
    import pandas as pd
    import numpy as np
    import sys
    df_batting = database_batting()
    PlayID = IDreturn_imp(firstname, lastname)
    #l_columns = list(df_batting.columns)
    #lnumber = l_columns.index(what)
    #print(lnumber)
    new_list = df_batting.query('playerID == @PlayID')
    return(np.array(list(new_list[what])))

def PlayerRecordPitching(firstname, lastname, what):
    import pandas as pd
    import numpy as np
    import sys
    df_pitching = pd.read_csv("/Users/yoshioyamazoe/Library/Mobile Documents/com~apple~CloudDocs/Python/github/baseball/baseballdatabank-master/core/Pitching.csv")
    PlayID = IDreturn_imp(firstname, lastname)
    new_list = df_pitching.query('playerID == @PlayID')
    return(np.array(list(new_list[what])))
