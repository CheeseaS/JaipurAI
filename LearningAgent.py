import numpy as np
import pandas as pd
import random
import math


# Note: in total, there is 6 actions for buying a single good, there is 6 actions for selling a type of good, 1 to buy
# all the camels, and 25492 for all the exchange combinations.
class LearningAgent:
    def __init__(self, q_matrix_location=None, exchange_action_table_location=None):
        self.learning_rate = 0.2
        self.discount_factor = 0.99
        self.epsilon = 0.9
        self.temperature = 4
        self.exchange_action_table = None

        self.previous_action_made = None
        self.previous_state = None

        # Probability of each action using Softmax. This array is defined to prevent multiple initializations.
        self.soft_max_prob = np.zeros(25505)

        # Initializes the q_net given the dimensions of the file location.
        if q_matrix_location is None:
            self.q_table = dict()
        else:
            self.load_state(q_matrix_location)

        # Initializes the exchange action table by either recreating it or using the file location.
        if exchange_action_table_location is None:
            self.create_exchange_action_table()
        else:
            self.exchange_action_table = np.mat(pd.read_csv(exchange_action_table_location, sep=',', header=None),
                                                dtype='int')

    # Saves the q_net model to a given file location.
    def save_state(self, location_string):
        np.save(location_string, self.q_table)

    # Loads the q_net model from a given file location.
    def load_state(self, location_string):
        self.q_table = np.load(location_string)

    # Creates a table of all the possible legal exchange combinations.
    def create_exchange_action_table(self):
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
    def give_reward(self, reward):
        if self.previous_state is not None:
            self.q_table[self.previous_state][self.previous_action_made] += self.learning_rate * reward

    # Takes a given board and the given players turn and calculates the current state of the player.
    @staticmethod
    def calculate_state(current_board, player):
        # The state is calculated by using the cards in hand, the cards in the market, and the number of each of the
        # good tokens.
        output = ''

        for current_type_in_hand in range(7):
            output += str(current_board.playerHands[player][current_type_in_hand])

        for current_type_in_market in range(7):
            output += str(current_board.market[current_type_in_market])

        # This hasn't been implemented yet in the game so this needs to be updated.
        for current_good_type in range(6):
            output += str(current_good_type)
        return output

    # Attempts to perform an action on the board given the index of the action and returns whether is succeeded or not.
    def attempt_action(self, current_board, player, action_index):

        # Checks if the action is to take a good from the market.
        if action_index < 6:
                action_succeeded = current_board.takegood(player, action_index)

        # Checks if the action is to sells goods from hand.
        elif action_index < 12:
            action_succeeded = current_board.sell(player, action_index - 6)

        # Checks if the action is to take all the camels from the market.
        elif action_index == 12:
            action_succeeded = current_board.takecamels(player)

        # Otherwise, the chosen action is to exchange goods and camels for goods.
        else:
            action_succeeded = current_board.exchangegoods(player, self.exchange_action_table[action_index - 13])

        return action_succeeded

    # Takes a given board and the given players turn and performs a move based on the q_net using epsilon greedy
    # learning.
    def make_move(self, current_board, player):
        self.previous_state = self.calculate_state(current_board, player)

        if self.previous_state not in self.q_table:
            self.q_table[self.previous_state] = np.zeros(25505) + 0.1
        expected_rewards = self.q_table[self.previous_state]

        # Decides to do the non-greedy move epsilon percent of the time.
        if random.choices([0, 1], [1 - self.epsilon, self.epsilon], k=1)[0] == 1:

            # For the non-greedy move, Softmax is used to decide the move.
            self.soft_max_prob = np.zeros(25505)

            for current_reward in range(25505):
                if self.temperature == 0:
                    self.soft_max_prob[current_reward] = expected_rewards[current_reward]
                else:
                    try:
                        self.soft_max_prob[current_reward] = math.exp(expected_rewards[current_reward]/self.temperature)
                    # The exponential function can overflow which is being caught and the value is being approximated.
                    except Exception:
                        if expected_rewards[current_reward] > 0:
                            self.soft_max_prob[current_reward] = 1000
                        elif expected_rewards[current_reward] == 0:
                            self.soft_max_prob[current_reward] = 1
                        else:
                            self.soft_max_prob[current_reward] = 0.01

            # Normalizes the array to get the probability of picking each action then creates a permutation based on the
            # the probability of picking each action.
            chosen_permutation = np.random.choice(25505, 25505, p=self.soft_max_prob / self.soft_max_prob.sum(),
                                                  replace=False)

            # Keeps attempting actions till one works.
            for action_being_attempted in  chosen_permutation:
                if self.attempt_action(current_board, player, action_being_attempted):
                    self.previous_action_made = action_being_attempted
                    break

        else:
            # Chooses the greed action.

            # Orders the actions based on their value.
            ordered_largest = np.argpartition(expected_rewards)[-1:]

            # Attempts best actions till one works and records which one succeeded.
            for current_action_attempt in ordered_largest:
                if self.attempt_action(current_board, player, current_action_attempt):
                    self.previous_action_made = current_action_attempt
                    break

        # Updates the expected value using the new state.
        new_state = self.calculate_state(current_board, player)
        if new_state not in self.q_table:
            self.q_table[new_state] = np.zeros(25505) + 0.1
            top_expected_reward = 0.1
        else:
            top_expected_reward = np.amax(self.q_table[new_state])

        # Updates the expected value in the previous state.
        self.q_table[self.previous_state][self.previous_action_made] += self.learning_rate * (
                    (self.discount_factor * top_expected_reward) - self.q_table[self.previous_state][
                     self.previous_action_made])

