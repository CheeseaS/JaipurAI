import RewardAgent
import Game

newGame = Game.Game()
#print ( not newGame.isgameover())
while ( not newGame.isgameover()):
    p1hand = newGame.gethand(0)
    market = newGame.getmarket()
    print(p1hand, market)
    tokens = newGame.getgtokens()

    move = RewardAgent.GenerateMove(p1hand, market, tokens)
    print(move)
    if move == 0:
        newGame.takegood(0,move[1])
    if move == 1:
        newGame.exchangegood(0,move[1])
    if move == 2:
        newGame.sell(0,move[1])
    if move == 3:
        newGame.takecamels(0)
    print(newGame.isgameover())
    if ( newGame.isgameover()):
        break
    p2hand = newGame.gethand(1)

    market = newGame.getmarket()
    tokens = newGame.getgtokens()
    print(p2hand, market)
    move = RewardAgent.GenerateMove(p2hand, market, tokens)
    print(move)
    if move == 0:
        newGame.takegood(1,move[1])
    if move == 1:
        newGame.exchangegood(1,move[1])
    if move == 2:
        newGame.sell(1,move[1])
    if move == 3:
        newGame.takecamels(1)

    print(newGame.getscore(0))
    print(newGame.getscore(1))

print (newGame.getscore(0))
print (newGame.getscore(1))

'''
#hand = [0,1,3,1,0,0,3]
hand = [0,0,1,1,0,0,1]
market = [1,1,3,0,0,0,0]
gtokens = [
    [1,1,1,1,1,1,2,3,4],
    [1,1,2,2,3,3,5],
    [1,1,2,2,3,3,5],
    [5,5,5,5,5],
    [5,5,5,6,6],
    [5,5,5,7,7]
    ]

move = RewardAgent.GenerateMove(hand,market,gtokens)
print (move)
'''