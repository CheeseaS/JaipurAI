import random
class Game:
    def __init__(self):
        self.deck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     1, 1, 1, 1, 1, 1, 1, 1,
                     2, 2, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3, 3, 3,
                     4, 4, 4, 4, 4, 4,
                     5, 5, 5, 5, 5, 5,
                     6, 6, 6, 6, 6, 6, 6, 6]
        random.shuffle(self.deck)

        self.bTokens = [[],
                        [],
                        []]
        for i in self.bTokens:
            random.shuffle(i)

        self.gtokens = [
            [1, 1, 1, 1, 1, 1, 2, 3, 4],
            [1, 1, 2, 2, 3, 3, 5],
            [1, 1, 2, 2, 3, 3, 5],
            [5, 5, 5, 5, 5],
            [5, 5, 5, 6, 6],
            [5, 5, 5, 7, 7]
        ]

        self.playerHands = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self.playerScores = [0, 0]
        self.playerBTScore = [0, 0]

        for i in range(5):
            self.playerHands[0][self.deck.pop()] += 1
            self.playerHands[1][self.deck.pop()] += 1

        self.market = [0, 0, 0, 0, 0, 0, 3]
        for i in range(2):
            self.market[self.deck.pop()] += 1

        return

    def sell(self, player, pos):
        minamnt = 1
        if pos > 2:
            minamnt = 2

        if self.playerHands[player][pos] < minamnt:
            return False

        if self.playerHands[player][pos] > 2:
            self.playerBTScore[player] += self.bTokens[self.playerHands[player][pos] - 2].pop()

        self.playerScores[player] += self.playerHands[player][pos]
        self.playerHands[player][pos] = 0

        return True

    def takecamels(self, player):
        for i in range(self.market[6]):
            self.market[self.deck.pop()] += 1
        self.playerHands[player][6] += self.market[6]
        self.market[6] = 0

        return True

    def takegood(self, player, pos):
        tmp = 0
        for i in self.playerHands[player]:
            if i != 6:
                tmp += self.playerHands[player][i]

        if self.market[pos] > 0 and tmp < 5:
            self.playerHands[player][pos] += 1
            self.market[pos] -= 1
            self.market[self.deck.pop()] += 1
            return True

        return False

    def exchangegood(self, player, goods):
        validexchange = True
        tmp = 0
        for i in range(7):
            tmp += goods[i]
            if (goods[i] < 0 and self.playerHands[player][i] < abs(goods[i])) \
                    or (goods[i] > 0 and self.market[i] < goods[i]):
                validexchange = False
                break

        if goods[6] > 0:
            validexchange = False

        if tmp != 0:
            validexchange = False

        if validexchange:
            for i in range(7):
                self.market[i] += -1 * goods[i]
                self.playerHands[player][i] += goods[i]

        return validexchange








