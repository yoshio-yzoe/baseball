import numpy as np
import tensorflow as tf
import tflearn

class GameStats(object):

    def __init__(self, homeTeamNameIndex, homeTeamScoreIndex, homeTeamStatsIndex, visitorTeamNameIndex, visitorTeamScoreIndex, visitorTeamStatsIndex):
        #parse the text file
        self.statsFile = open("baseball2016.txt", "r")
        self.topArray = []
        self.sideArray = []
        self.sc = np.zeros((30,30,30), np.int32)
        self.sc[:,:,:] = -1
        self.am = np.zeros((30,30), np.float32)
        self.gameList = []

        seenTeams = []
        for line in self.statsFile:
            token = line.split(',')  #tokenize the string
            tokenIndex = [homeTeamNameIndex, homeTeamScoreIndex, visitorTeamNameIndex, visitorTeamScoreIndex] + [i for i in homeTeamStatsIndex] + [i for i in visitorTeamStatsIndex]
            attributes = dict()

            for i in range(len(token)):
                if(i in tokenIndex):
                    attributes[i] = self.removeQuotes(token[i])

            self.addScore(attributes[homeTeamNameIndex], attributes[visitorTeamNameIndex], attributes[homeTeamScoreIndex], attributes[visitorTeamScoreIndex])
            self.addGame(attributes[homeTeamNameIndex], attributes[homeTeamScoreIndex], [attributes[i] for i in homeTeamStatsIndex], attributes[visitorTeamNameIndex], attributes[visitorTeamScoreIndex], [attributes[i] for i in visitorTeamStatsIndex])

            if(attributes[homeTeamNameIndex] not in seenTeams):
                seenTeams.append(attributes[homeTeamNameIndex])

        self.buildAvgMatrix()
        self.statsFile.close()
        #self.gameList = [bin(2**i)[2:].zfill(len(seenTeams)) if x == seenTeams[i] else x for i in range(len(seenTeams)) for x in self.gameList]
        # take the teams and convert the indexes of the order that they appeared in into the hot one format by rasiing
        # 2 to the power of them and then converting them into binary.
        seenTeamsDict = {k: v for v, k in enumerate(seenTeams)}
        temp = []
        for x in self.gameList:
            tempi = []
            for z in x:
                if(z in seenTeams):
                    tempi.append(bin(2**seenTeamsDict[z])[2:].zfill(len(seenTeamsDict)))
                else:
                    tempi.append(z)
            temp.append(tempi)
        self.gameList = temp

    def removeQuotes(self, string):
        if (string.startswith('"') and string.endswith('"')) or (string.startswith("'") and string.endswith("'")):
            return string[1:-1]
        return string

    def addGame(self, team1, score1, stats1, team2, score2, stats2):
        self.gameList.append([team1, score1, stats1, team2, score2, stats2])

    #give it two teams, the scores, and it will add it to the matrix
    def addScore(self, team1, team2, score1, score2):
        '''
        for a team in top array, the index in the array corrisponds to the matrix column there located in
        for a team in side array, the index in the array corrisponds to the matrix row there located in
        '''
        #team 1 score entry
        try:
            row = self.sideArray.index(team2)

        except:
            self.sideArray.append(team2)
            row = self.sideArray.index(team2)

        try:
            col = self.topArray.index(team1)
        except:
            self.topArray.append(team1)
            col = self.topArray.index(team1)
        temp = self.sc[row, col]
        counter = 0
        for e in temp:
            if (e == -1):
                temp[counter] = score1
                break
            counter += 1
        self.sc[row, col] = temp

        #team 2 score entry
        try:
            row = self.sideArray.index(team1)
        except:
            self.sideArray.append(team1)
            row = self.sideArray.index(team1)

        try:
            col = self.topArray.index(team2)
        except:
            self.topArray.append(team2)
            col = self.topArray.index(team2)
        temp = self.sc[row, col]
        counter = 0
        for e in temp:
            if (e == -1):
                temp[counter] = score2
                break
            counter += 1
        self.sc[row, col] = temp

    #returns the score(s) for match up
    def getScore(self, team1, team2, gameSelect = None):
        print(team1, team2)
        try:
            score1 = self.sc[self.sideArray.index(team2), self.topArray.index(team1)]
            score2 = self.sc[self.sideArray.index(team1), self.topArray.index(team2)]
            if (gameSelect == None):
                print(team1, score1)
                print(team2, score2)
            else:
                print(team1, score1[gameSelect])
                print(team2, score2[gameSelect])
        except:
            print('Invalid input of teams')

    def getGameList(self):
        return self.gameList

    #constructs a matrix of the avg score in a matchup
    def buildAvgMatrix(self):
        for col in range(len(self.sc[:,0])):   #depth
            for row in range(len(self.sc[0, :])):  #width
                tempScore = self.sc[row, col]
                avgScore = 0.0
                count = 0.0
                for j in tempScore:
                    if (j != -1):
                        avgScore += j
                        count += 1
                    else:
                        break
                try:
                    avgScore = avgScore / count
                except:
                    avgScore = -1
                self.am[row, col] = avgScore

    #get the value of the avg score for a match up
    def getAvgScore(self, team1, team2):
        try:
            score1 = self.am[self.sideArray.index(team2), self.topArray.index(team1)]
            score2 = self.am[self.sideArray.index(team1), self.topArray.index(team2)]
            print(team1, score1)
            print(team2, score2)
        except:
            print('Invalid input of teams')


if __name__ == '__main__':
    tf.reset_default_graph()

    # Parse the game files and grab the stats we want
    # the indexes are put in the order: homeTeamName, homeTeamScore, homeTeamStats, awayName, awayScore, awayStats
    stats = GameStats(3, 10, [51, 55], 6, 9, [23, 27])
    gameList = stats.getGameList() # get the list of games

    # the input layer needs to have the same dimensions as our input (in this case the teams)
    net = tflearn.input_data(shape=[None, len(gameList[0][0])], name='input')
    # next we have the hidden layer it is the feature matrix the size is arbitrary.
    # I chose 15 becasue that is what the matrix factorization feature size is set to.
    net = tflearn.fully_connected(net, 15)
    # The output layer
    net = tflearn.fully_connected(net, len(gameList[0][2]))

    net = tflearn.regression(net, name='target', learning_rate=0.9)

    # Note(daniel): right now we don't care what teams played eachother (we may in the future) therefore all of the teams are put
    # into one array.

    # take only the team names and split them into individual parts (ie 0100 becomes [0], [1], [0], [0])
    NNInput = [list(i[x]) for i in gameList for x in range(len(i)) if x == 0 or x == 3]
    NNInput = np.array(NNInput)

    # take only the stats for each team and put them into an array
    NNOutput = [[7, 7] for i in gameList for x in range(len(i)) if x == 2 or x == 5]
    NNOutput = np.array(NNOutput)

    # Define model
    model = tflearn.DNN(net)
    # Start training (apply gradient descent algorithm)
    model.fit(NNInput, NNOutput, validation_set=0.1, n_epoch=20, show_metric=True)

    # Prediction Test
    from tqdm import tqdm_notebook

    # trying to write all of the data seems to crash my browser
    # so I'm dumping the raw output to a file to read later.
    file = open('netOutput.txt', 'w')

    testIndex = 0
    closest = 1000
    for i in tqdm_notebook(range(len(NNInput))):
        predict = model.predict([NNInput[i]])

        if(((predict[0][0]-float(NNOutput[i][0]))+(predict[0][1]-float(NNOutput[i][1])))**2 < closest):
            closest = ((predict[0][0]-float(NNOutput[i][0]))+(predict[0][1]-float(NNOutput[i][1])))**2
            testIndex = i

        file.write("hits, RBI")
        file.write("\n")
        file.write(str(predict))
        file.write("\n")
        file.write(str(NNOutput[i]))
        file.write("\n")

    file.close()

    print("hits, RBI")
    print(testIndex)
    print(model.predict([NNInput[testIndex]]))
    print(NNOutput[testIndex])
