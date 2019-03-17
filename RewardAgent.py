#import Game
import copy

# reward based agent
def GenerateMove(hand, market, tokens):
    #print(hand)
    #print(market)
    #handscore = max(goodVal)
    handScore = scoreHand(hand,tokens)
    handSz = 0
    getScore = 0
    swapscore = 0
    for i in range(0,6):
        handSz += hand[i]
    #print(cardNo)
    # check valid moves
    if handSz < 7:
        getScore = getCard(hand,market,tokens)

    if handSz > 1:
        swapScore = SwapCards(hand, market, tokens)
    print (getScore)
    print (swapScore)

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
            if hand[i] >= 5:
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

    for j in posSwaps:
        temphand = copy.deepcopy(hand)
        temphand[j] = temphand[j] + market[j]
        tempScore = scoreHand(temphand, tokens)
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
    if handSz < 7:
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
        #print(i, handDiff, getting)
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


    #print (swap)
# if (market[i] >= 2)

# camels + goods[!max]
# if (swap > get)
# do swap
# if ((getScore < handScore) and (handscore > camelNum)
# sell max(good)
# else
# take camels




