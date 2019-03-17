from multiprocessing import Pool, Manager
from Game import Game
from LearningAgent import LearningAgent


def run_game(current_agent):
    current_game = Game()

    while True:
        current_agent.make_move(current_game,0)
        if current_game.isGameOver():
            break
        current_agent.make_move(current_game,1)
        if current_game.isGameOver():
            break


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

jobs = (['test.csv','first_run.csv',100], ['test.csv','second_run.csv',100])

def pool_handler():
    p = Pool(2)
    return p.map(run_batch,jobs)

if __name__ == '__main__':
    print(pool_handler())
