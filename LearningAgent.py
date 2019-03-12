import numpy as np
import pandas as pd
import random
import math
from keras import models
from keras import layers
from keras import load_model

# Note: in total, there is 6 actions for buying a single good, there is 6 actions for selling a type of good, 1 to buy
# all the camels, and 25492 for all the exchange combinations.
class LearningAgent:
    def __init__(self, qnet_location=None, exchange_action_table_location=None):
        self.qnet_learning_rate = 0.2
        self.qnet_discount_factor = 0.9
        self.epsilon = 0.9
        self.temperature = 4
        self.exchange_action_table = None

        self.previousactionmade = None
        self.previousactionprobabilities = None
        self.previousstate = None

        # Initializes the q_net given the dimensions of the file location.
        if qnet_location is None:
            self.qnet = models.Sequential()
            self.q_net.add(layers.Dense(21, activation='relu', input_shape=(1,)))
            for current_layer in [21, 42, 42, 42, 25505]:
                self.q_net.add(layers.Dense(current_layer, activation='relu'))
            self.q_net.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
        else:
            self.loadstate(qnet_location)

        # Initializes the exchange action table by either recreating it or using the file location.
        if exchange_action_table_location is None:
            self.createexchangeactiontable()
        else:
            self.exchange_action_table = np.mat(pd.read_csv(exchange_action_table_location, sep=',', header=None),
                                                dtype='int')

    # Saves the q_net model to a given file location.
    def savestate(self, locationstring):
        self.qnet.save(locationstring)

    # Loads the q_net model from a given file location.
    def loadstate(self, locationstring):
        self.qnet = load_model(locationstring)

    # Creates a table of all the possible legal exchange combinations.
    def createexchangeactiontable(self):
        self.exchange_action_table = np.zeros((25492, 7))
        count = 0
        for leather in range(-5, 6):
            for silk in range(-5, 6):
                for spice in range(-5, 6):
                    for silver in range(-5, 6):
                        for gold in range(-5, 6):
                            for gems in range(-5, 6):
                                for camels in range(-5, 1):
                                    if leather + silk + spice + silver + gold + gems + camels == 0:
                                        if abs(leather) + abs(silk) + abs(spice) + abs(silver) + abs(gold) + abs(
                                                gems) + abs(camels) in {2, 4, 6, 8, 10}:
                                            self.exchange_action_table[count, 0] = leather
                                            self.exchange_action_table[count, 1] = silk
                                            self.exchange_action_table[count, 2] = spice
                                            self.exchange_action_table[count, 3] = silver
                                            self.exchange_action_table[count, 4] = gold
                                            self.exchange_action_table[count, 5] = gems
                                            self.exchange_action_table[count, 6] = camels
                                            count += 1

    # Gives a reward for the previous state and action performed by the learning agent.
    def givereward(self, reward):
        if self.previousactionmade is not None:
            self.previousactionprobabilities[self.previousactionmade] += self.qnet_learning_rate * (
                        reward - self.previousactionprobabilities[self.previousactionmade])
            self.qnet.train_on_batch(self.previousstate,self.previousactionprobabilities)


    # Takes a given board and the given players turn and calculates the current state of the player.
    def calculatestate(self, currentboard, player):
        # The state is calculated by using the number of cards remaining, the cards in hand, the cards in the
        # market, and the number of each of the good tokens.
        # The values have been standardized to keep a consistent range between 0 and 1.
        output = np.zeros(21)

        for currenttypeinhand in range(6):
            output[currenttypeinhand] = currentboard.playerHands[player][currenttypeinhand] / 7
        self.previousstate[6] = currentboard.playerHands[player][6] / 11
        for currenttypeinmarket in range(7):
            output[currenttypeinmarket + 7] = currentboard.market[currenttypeinmarket]
        output[14] = len(currentboard.deck) / 55

        # This hasn't been implemented yet in the game so this needs to be updated.
        for currentgoodtype in range(6):
            output[15 + currentgoodtype] = 0.42
        return output


    # Takes a given board and the given players turn and performs a move based on the q_net using epsilon greedy
    # learning.
    def makemove(self, currentboard, player):
        self.previousstate = self.calculatestate(currentboard, player)

        # Calculate the expected reward for each action given the current state.
        self.previousactionprobabilities = self.qnet.predict(self.previousstate)[0]

        # Decides to do the non-greedy move epsilon percent of the time.
        if random.choices([0, 1], [1 - self.epsilon, self.epsilon], k=1)[0] == 1:
            actionattemptorder = np.random.choice(4, 4, replace=False)
            for currentattempt in actionattemptorder:
                if currentattempt == 0:
                    # Trying to take a good from the market. This action can't fail unless the hand is full.
                    self.previousactionmade = random.randint(0,5)
                    if currentboard.takegood(player, self.previousactionmade):
                        break
                elif currentattempt == 1:
                    # Trying to sell gods from hand.  This action can fail if the player doesn't have enough of the
                    # good.
                    sellattemptorder = np.random.choice(6, 6, replace=False)
                    temp = True
                    for sellattemp in sellattemptorder:
                        if currentboard.sell(player,sellattemp):
                            temp = False
                            self.previousactionmade = sellattemp + 6
                            break
                    if not temp:
                        break

                elif currentattempt == 2:
                    # Trying to take all the camels. This action can't fail unless the market has no camels.
                    self.previousactionmade = 12
                    if currentboard.takecamels(player):
                        break

                else:
                    # Trying to exchange goods and camels for goods.
                    exchangeattemptorder = np.random.choice(25492, 25492, replace=False)
                    temp = True
                    for exchangeattemp in exchangeattemptorder:
                        if currentboard.exchangegoods(player,self.exchange_action_table[exchangeattemp]):
                            temp = False
                            self.previousactionmade = exchangeattemp + 13
                            break
                    if not temp:
                        break
        else:
            # Chooses the greed action.

            # Orders the actions based on their value.
            ordered_largest = np.argpartition(self.previousactionprobabilities)[-1:]
            for currentactionattemp in ordered_largest:
                # Checks if the action is to take a good from the market.
                if currentactionattemp < 6:
                    if currentboard.takegood(player, urrentactionattemp):
                        self.previousactionmade = currentactionattemp
                        break
                # Checks if the action is to sells goods from hand.
                elif currentactionattemp < 12:
                    if currentboard.sell(player, currentactionattemp - 6):
                        self.previousactionmade = currentactionattemp
                        break
                # Checks if the action is to take all the camels from the market.
                elif currentactionattemp == 12:
                    if currentboard.takecamels(player):
                        self.previousactionmade = 12
                        break
                # Otherwise, the chosen action is to exchange goods and camels for goods.
                else:
                    if currentboard.exchangegoods(player, self.exchange_action_table[currentactionattemp - 13]):
                        self.previousactionmade = currentactionattemp
                        break

        # Update the value for performing that action in the now previous state.
        update_value = self.qnet_learning_rate * (reward + (self.qnet_discount_factor * np.amax(
            self.qnet.predict(self.calculatestate(currentboard, player))[0])) -
                                                  self.previousactionprobabilities[self.previousactionmade])
        self.previousactionprobabilities[self.previousactionmade] += update_value
        self.qnet.train_on_batch(self.previousstate,self.previousactionprobabilities)
        self.previousactionprobabilities -= update_value

