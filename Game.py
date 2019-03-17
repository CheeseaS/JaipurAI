import random
class Game:

    #initilize game "board"
    def __init__(self):
        # The deck. values represent positions in the player's hand and the market
                     # 0 - leather
        self.deck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     # 1 - spice
                     1, 1, 1, 1, 1, 1, 1, 1,
                     # 2 - cloth
                     2, 2, 2, 2, 2, 2, 2, 2,
                     # 3 - sliver
                     3, 3, 3, 3, 3, 3,
                     # 4 - gold
                     4, 4, 4, 4, 4, 4,
                     # 5 - diamonds
                     5, 5, 5, 5, 5, 5,
                     # 6 - camels
                     6, 6, 6, 6, 6, 6, 6, 6]
        random.shuffle(self.deck)

        # Goods tokens, sorted by type into sub-lists:
        # leather, spice, cloth, silver, gold, diamonds
        self.gTokens = [[1, 1, 1, 1, 1, 1, 2, 3, 4],
                        [1, 1, 2, 2, 3, 3, 3],
                        [1, 1, 2, 2, 3, 3, 3],
                        [5, 5, 5, 5, 5],
                        [5, 5, 5, 6, 6],
                        [5, 5, 5, 7, 7]]

        # Bonus tokens, sorted into sub-lists based on the number of items being sold (3, 4, 5)
        self.bTokens = [[1, 1, 2, 2, 2, 3, 3],
                        [4, 4, 5, 5, 6, 6],
                        [8, 8, 9, 10, 10]]
        for i in self.bTokens:
            random.shuffle(i)

        # Player's hands, each position in the sub-lists represents the number of that card type in the player's
        # hand: leather, spice, cloth, silver, gold, diamonds, camels
        self.playerHands = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        # Player score and "hidden" bonus score
        self.playerScores = [0, 0]
        self.playerBTScores = [0, 0]

        # Each player starts with 5 cards
        for i in range(5):
            self.playerHands[0][self.deck.pop()] += 1
            self.playerHands[1][self.deck.pop()] += 1

        # The market always starts with 3 camels
        self.market = [0, 0, 0, 0, 0, 0, 3]
        # add two more cards to the market
        for i in range(2):
            self.market[self.deck.pop()] += 1

        return

    # Sell all the goods of a specific type.
    # pos indicates type: 0: leather, 1: spice, 2: cloth, 3: silver, 4: gold, 5: diamonds
    # 6 is not a valid position value for this move, you can't sell camels.
    def sell(self, player, pos):
        # You can't sell the more valuable goods if you have less that 2
        minamnt = 1
        if pos > 2:
            minamnt = 2

        # Are they trying to sell camels? That's not valid
        if self.playerHands[player][pos] < minamnt or pos == 6:
            return False

        # Grab a goods token for each good sold
        for i in range(self.playerHands[player][pos]):
            if self.gTokens[pos]:
                self.playerScores += self.gTokens[pos].pop()

        # If they are selling 3 or more then they get BONUS TOKENS!!! YAY
        if self.playerHands[player][pos] > 2 and [self.playerHands[player][pos] - 2]:
            self.playerBTScores[player] += self.bTokens[self.playerHands[player][pos] - 2].pop()

        self.playerHands[player][pos] = 0

        return True

    # Moves all of the camels in the market into the player's hand (herd)
    def takecamels(self, player):
        camels = self.market[6]
        self.playerHands[player][6] += self.market[6]
        self.market[6] = 0
        for i in range(camels):
            if self.deck:
                self.market[self.deck.pop()] += 1
        return True

    # Moves one good into the player's hand.
    # pos indicates the good type: 0: leather, 1: spice, 2: cloth, 3: silver, 4: gold, 5: diamonds
    def takegood(self, player, pos):
        tmp = 0
        # count the number of cards already in the user's hand, they can't have more that 7 non-camel cards
        for i in self.playerHands[player]:
            # camels don't count
            if i != 6:
                tmp += self.playerHands[player][i]

        # If the good is available in the market AND they have less than 7 cards then let them take the good
        if self.market[pos] > 0 and tmp < 7 and pos != 6:
            self.playerHands[player][pos] += 1
            self.market[pos] -= 1
            if self.deck:
                self.market[self.deck.pop()] += 1
            return True

        return False

    # Lets the player exchange goods.
    # The goods parameter should be an array/list where a positive value indicates that the player wants that many
    # of that good type and a negative value indicates that the player is offering that good in the trade.
    # good types by position: 0: leather, 1: spice, 2: cloth, 3: silver, 4: gold, 5: diamonds, 6: camels
    def exchangegood(self, player, goods):
        validexchange = True
        tmp = 0
        # Determine if the trade is valid
        for i in range(7):
            # Add up the goods being traded/received to determine if the trade is valid
            tmp += goods[i]
            # check if they are trading a good that they don't have or requesting a good that is not at market
            if (goods[i] < 0 and self.playerHands[player][i] < abs(goods[i])) \
                    or (goods[i] > 0 and self.market[i] < goods[i]):
                validexchange = False
                break

        # You can't take camels with this move
        if goods[6] > 0:
            validexchange = False

        # The player must trade as many good as they are getting and vice-versa
        if tmp != 0:
            validexchange = False

        # If the exchange is valid the we will let it go through
        if validexchange:
            for i in range(7):
                self.market[i] += -1 * goods[i]
                self.playerHands[player][i] += goods[i]

        return validexchange

    # Checks if the game has ended
    def isgameover(self):
        if not self.deck:
            return True

        emptystacks = 0
        for i in self.gTokens:
            if not i:
                emptystacks += 1
        if emptystacks > 2:
            return True

        return False
