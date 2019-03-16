#import Game
import copy

# reward based agent
def GenerateMove(hand, market, tokens):
    print(hand)
    print(market)
    #handscore = max(goodVal)
    handScore = scoreHand(hand,tokens)
    cardNo = 0
    getScore = 0
    swapscore = 0
    for i in range(0,6):
        cardNo += hand[i]
    #print(cardNo)
    # check valid moves
    if (cardNo < 7):
        getScore = getCard(hand,market,tokens)
    swapCheck = True
    if swapCheck == True:
        swapscore = SwapCards(hand, market, tokens, cardNo)
    #print(handScore)
    #print(getScore)
    return "foo"

# check score in hand
def scoreHand(hand, tokens):
    #print(tokens)
    #print(hand)
    maxScore = 0
    # for each good in hand:
    for i in range(5, -1, -1):
        #print(i)
        sum = 0
        if hand[i] != 0:
            if (tokens[i]):
                stSz = len(tokens[i]) - 1
                # check current point value for good
                for j in range(0,hand[i]):
                    sum += tokens[i][(stSz - j)]
            # if bonus value applies, add value
            if hand[i] == 3:
                sum += 2
            if hand[i] == 4:
                sum += 5
            if hand[i] == 5:
                sum += 9
            if sum > maxScore:
                maxScore = sum
    return maxScore

# check pick up value
# for each good in market
# generate hands based on player hand plus 1 good in market place
# store max score and associated move
def getCard(hand, market, tokens):
    maxScore = (0,0)
    # for valid moves generate handscores:
    for i in range(6, -1,-1):
        if market[i] != 0:
            temphand = copy.deepcopy(hand)
            temphand[i] += 1
            tempScore = scoreHand(temphand,tokens)
            if tempScore > maxScore[0]:
                maxScore = (tempScore, i)
    return maxScore

# check swap value
def SwapCards(hand, market, tokens, cardNo):
    maxScore = 0
    # determine cards to swap
    validSwaps = []
    for i in range (0,6):
        if market[i] > 1:
            validSwaps.append(i)

    for j in validSwaps:
        temphand = copy.deepcopy(hand)
        #print(temphand)
        if (cardNo + market[j]) < 8:
            temphand[j] = temphand[j] + market[j]
            print(temphand)
            tempScore = scoreHand(temphand, tokens)
            print(tempScore)
    #break swaps into cases, swap < camel and swap > camel
    # hand > 7







# if (market[i] >= 2)

# camels + goods[!max]
# if (swap > get)
# do swap
# if ((getScore < handScore) and (handscore > camelNum)
# sell max(good)
# else
# take camels




