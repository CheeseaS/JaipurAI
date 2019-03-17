from Game import Game
from LearningAgent import LearningAgent

def run_game(current_agent):
    current_game = Game()

    while True:
        current_agent.make_move(current_game,0)
        if current_game.isgameover():
            current_agent.give_reward(10000 * (current_game.playerScores[0] + current_game.playerBTScores[0]))
            break
        current_agent.make_move(current_game,1)
        if current_game.isgameover():
            current_agent.give_reward(10000 * (current_game.playerScores[1] + current_game.playerBTScores[1]))
            break

    if current_game.playerHands[0][6] > current_game.playerHands[1][6]:
        current_game.playerBTScores[0] += 5
    elif current_game.playerHands[0][6] < current_game.playerHands[1][6]:
        current_game.playerBTScores[1] += 5

    first_player_score = current_game.playerScores[0] + current_game.playerBTScores[0]
    second_player_score = current_game.playerScores[1] + current_game.playerBTScores[1]
    if first_player_score > second_player_score:
        return first_player_score, second_player_score, 0
    elif first_player_score < second_player_score:
        return first_player_score, second_player_score, 1
    else:
        if current_game.playerBTScores[0] > current_game.playerBTScores[1]:
            return first_player_score, second_player_score, 0
        elif current_game.playerBTScores[0] < current_game.playerBTScores[1]:
            return first_player_score, second_player_score, 1
        else:
            return first_player_score, second_player_score, 2


def run_batch(location_string, result_string, batch_size):
    batch_average = [0,0]
    winners = [0,0,0]
    current_agent = LearningAgent(q_matrix_location=location_string)
    for current_game in range(batch_size):
        results = run_game(current_agent)
        batch_average[0] += results[0]
        batch_average[1] += results[1]
        winners[results[2]] += 1
    current_agent.save_state(result_string)
    return batch_average, winners


current_agent = LearningAgent(q_matrix_location='saved_agent.csv.npy',exchange_action_table_location='exchange_translation_matrix.csv')
print(run_game(current_agent))
current_agent.save_state('saved_agent.csv')