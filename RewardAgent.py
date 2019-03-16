#import Game
import copy

# reward based agent
def GenerateMove(hand, market, tokens):


    handscore = scoreHand(hand,tokens)
    print(market)
    print(hand)
    handScore = handscore
    getScore = getCard(hand,market,tokens)
    print(handscore)
    print(getScore)
    return "foo"

# check score in hand
def scoreHand(hand, tokens):
    #print(tokens)
    #print(hand)
    maxScore = 0
    # for each good in hand:
    for i in range (0,6):
        sum = 0
        if hand[i] != 0:
            if (tokens[i]):
                stSz = len(tokens[i]) - 1
                # check current point value for good
                for j in range(0,hand[i]):

                    sum += tokens[i][(stSz - j)]
            #print (hand[i])
            if hand[i] == 3:
                #print("+2")
                sum += 2
            if hand[i] == 4:
                #print("+5")
                sum += 5
            if hand[i] == 5:
                #print("+9")
                sum += 9
            #print(sum)
            if sum > maxScore:
                maxScore = sum
    return maxScore

def getCard(hand, market, tokens):
    maxScore = (0,0)
    for i in range(0,6):
        if market[i] != 0:
            temphand = copy.deepcopy(hand)
            temphand[i] +=1
            #print(temphand)
            tempScore = scoreHand(temphand,tokens)
            if tempScore > maxScore[0]:
                maxScore = (tempScore,i)
    return maxScore



# if bonus value applies, add value
# handscore = max(goodVal)

# check valid moves
# for valid moves generate handscores:
# check pick up value
# for each good in market
# generate hands based on player hand plus 1 good in market place
# store max score and associated move
# check swap value
# if (market[i] >= 2)
# determine cards to swap
# camels + goods[!max]
# if (swap > get)
# do swap
# if ((getScore < handScore) and (handscore > camelNum)
# sell max(good)
# else
# take camels




