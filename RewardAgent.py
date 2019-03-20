#import Game
import copy


#fix invalid sales

# reward based agent
def GenerateMove(hand, market, tokens):
    #handscore = max(goodVal)


    for h in range (0,5):
        if hand[h] >=5:
            return (3,h)
    getScore = (0,0)
    swapScore = (0,0)
    scoreMat = [-1 , -1, -1, -1]
    handSz = 0
    for i in range(0,6):
        handSz += hand[i]
    handScore = scoreHand(hand,tokens)
    # check valid moves
    if handSz < 7:
        getScore = getCard(hand, market, tokens)
        scoreMat[0] = getScore[0]
    if handSz > 1:
        swapScore = SwapCards(hand, market, tokens)
        if swapScore[1] == [0,0,0,0,0,0,0]:
            scoreMat[1] = -1
        else:
            scoreMat[1] = swapScore[0]
    sellgood = sell(hand,tokens)
    scoreMat[2] = sellgood[0]
    scoreMat[3] = market[6]

    move = scoreMat.index(max(scoreMat))

    if move == 0 and getScore[1] == -1:
        for i in range (5,-1,-1):
            if market[i] >0:
                return (0,i)

    if move == 0:
        if getScore[1] == -1:
            print("get fail")
        return (move,getScore[1])
    if move == 1:
        if swapScore[1] == -1:
            print("swap fail")
        return (move,swapScore[1])
    if move == 2:
        if sellgood[1] == -1:
            print("sell fail")
        return (move, sellgood[1])
    if move == 3:
        return (move,0)


    #return "foo"

# check score in hand
def scoreHand(hand, tokens):
    maxScore = 0
    pos= -1
    # for each good in hand:
    for i in range(5, -1, -1):
        #print(i)
        sum = 0
        if hand[i] != 0:
            if (tokens[i]):
                stSz = len(tokens[i]) - 1
                # check current point value for good
                for j in range(0,hand[i]):
                    if stSz - j >= 0:
                        sum += tokens[i][(stSz - j)]
            # if bonus value applies, add value
            if hand[i] == 3:
                sum += 2
            if hand[i] == 4:
                sum += 5
            if hand[i] >= 5:
                sum += 9
            if sum > maxScore:
                maxScore = sum
                pos = i
    return (maxScore,pos)

# check pick up value
# for each good in market
# generate hands based on player hand plus 1 good in market place
# store max score and associated move
def getCard(hand, market, tokens):
    maxScore = 0
    validtakes = []
    besttrade = -1
    # for valid moves generate handscores:
    for i in range (5, -1,-1):
        if market[i] > 0:
            validtakes.append(i)

    for j in validtakes:
        temphand = copy.deepcopy(hand)
        temphand[j] += 1

        tempScore = 0
        if (tokens[j]):
            stSz = len(tokens[j]) - 1
            # check current point value for good
            for k in range(0, hand[j]):
                if stSz-k >= 0:
                    tempScore += tokens[j][(stSz - k)]

        if tempScore > maxScore:
            maxScore = tempScore
            besttrade = j
    #if besttrade == -1:
        #print("get failed")
    return maxScore,besttrade

# check swap value
def SwapCards(hand, market, tokens):
    maxScore = 0
    bestSwap = -1
    GTS = False
    # determine cards to swap
    posSwaps = []
    secondCheck(bestSwap, hand)
    for i in range (0,6):
        if market[i] > 1:
            posSwaps.append(i)
    if not posSwaps:
        return (-1,[])
    for j in posSwaps:
        temphand = copy.deepcopy(hand)
        temphand[j] = temphand[j] + market[j]
        temp = scoreHand(temphand, tokens)
        tempScore = temp[0]
        if tempScore > maxScore:
            maxScore = tempScore
            bestSwap = j

    swap = [0,0,0,0,0,0,0]
    swap[bestSwap] = market[bestSwap]

    balanceSwap(swap,temphand)
    for i in range(0,7):
        temphand[i] = hand[i] + swap[i]
    #all swaps can be done by camels
    if not GTS and hand[6] > market[bestSwap]:
        qty = market[bestSwap]
        temphand[6] -= qty

    if swapcheck(swap,hand, market) == False:
        #print("invalid swap")
        return (-1,-1)
    return (maxScore,swap)
    #handsize check
    #find cards to swap
    #break swaps into cases, swap < camel and swap > camel
    # hand > 7


    #needed GTS swap
        #find excess number
        #find goods to offset excess
        #use camels to offset the rest
    #goods swap
        #find number of goods to swap for bestSwap
            #sum goods from 0-6 until
def balanceSwap(swap, hand):
    handSz = 0
    getting = swap.index(max(swap))

    for i in range(0,6):
        handSz += hand[i]
    if handSz > 7:
        overLimit(swap, hand,handSz,getting)
    else:
        simpleSwap(swap, hand, getting)
    sum = 0
    for i in range(0,7):
        sum += swap[i]
    if sum != 0:
        swap[getting] -= sum

def overLimit(swap, hand, handSz, getting):
    handDiff = handSz - 7
    i = 0
    while (handDiff > 0) and (i < 7):
        if i == getting:
            i += 1
        else:
            good = hand[i]
            if good == 0:
                i += 1
                continue
            if good < handDiff:
                swap[i] = -good
                handDiff -= good
                i += 1
                continue
            if good >= handDiff:
                swap[i] = -handDiff
                handDiff = 0
    return swap

#need swap format

def secondCheck(bestSwap, hand):
    swapNo = 0
    if bestSwap == -1:
        return False
    for i in range(0,7):
        if i != bestSwap:
            swapNo += hand[i]
    if swapNo < 2:
        return False
    return True

def simpleSwap(swap, hand, getting):
    #print(swap, hand)
    if (hand[6] > getting):
        swap[6] = -swap[getting]
    else:
        swap[6] = -hand[6]
        remaining = swap[getting] + swap[6]
        i = 0
        while (remaining > 0) and (i < 7):
            if i == getting:
                i += 1
            else:
                good = hand[i]
                if good <= 0:
                    i += 1
                    continue
                if good < remaining:
                    swap[i] = -good
                    remaining -= good
                    i += 1
                    continue
                if good >= remaining:
                    swap[i] = -remaining
                    remaining = 0


def swapcheck(swap, hand, market):
    tmp = 0
    for i in range (0,7):
        tmp += hand[i]
    if tmp != 0:
        return False
    if (max(swap) < 2):
        return False
    for j in range (0,6):
        tmp = hand[j] + swap[j]
        if tmp <= -1:
            return False
    return True

def sell(hand, tokens):
    maxpts = 0
    good = -1
    for i in range(0,6):
        if (i > 2) and (hand[i] < 2):
            continue
        sum = 0
        if hand[i] != 0:
            tmp = hand[i]
            stackSz = len(tokens[i]) - 1

            for j in range (0,tmp):
                if stackSz - j >= 0:
                    sum += tokens[i][(stackSz - j)]
        if sum > maxpts:
            maxpts = sum
            good = i
        #if good == -1:
            #print ("sell failure")
    return (maxpts,good)
# if (market[i] >= 2)




# camels + goods[!max]
# if (swap > get)
# do swap
# if ((getScore < handScore) and (handscore > camelNum)
# sell max(good)
# else
# take camels




