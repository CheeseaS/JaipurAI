#import Game


# reward based agent
def GenerateMove(hand, market, tokens):


    handscore = scoreHand(hand,tokens)
    print(handscore)
    return "foo"


def scoreHand(hand, tokens):
    #print(tokens)
    print(hand)
    maxScore = 0
    for i in range (0,6):
        if hand[i] != 0:
            if (tokens[i]):
                sum = 0
                stSz = len(tokens[i]) -1
                for j in range(0,hand[i]):
                    sum += tokens[i][(stSz -j)]
            if sum > maxScore:
                maxScore = sum
    return maxScore
# check score in hand
# for each good in hand:
# check current point value for good
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




