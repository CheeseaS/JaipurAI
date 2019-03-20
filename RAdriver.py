
from Game import Game
import RewardAgent

newGame = Game()

#print ( not newGame.isgameover())
while ( not newGame.isgameover()):

    p1hand = newGame.gethand(0)
    market = newGame.getmarket()
    #print(p1hand, market, "p2 hand, market")
    tokens = newGame.getgtokens()

    move = RewardAgent.GenerateMove(p1hand, market, tokens)
    p1movecheck = False
    #print(move, "move")
    player = 0
    if move[0] == 0:
        p1movecheck = newGame.takegood(player, move[1])
    if move[0] == 1:
        p1movecheck = newGame.exchangegood(player, move[1])
    if move[0] == 2:
        p1movecheck = newGame.sell(player, move[1])
    if move[0] == 3:
        p1movecheck = newGame.takecamels(player)


    if not p1movecheck:
        print(p1movecheck, "move: ", move[0], "player: ", player, "arg: ", move[1], "hand: ", p1hand, "market: ", market)
        break
    if ( newGame.isgameover()):
        break
    player = 1
    p2movecheck = False
    p2hand = newGame.gethand(1)
    market = newGame.getmarket()
    tokens = newGame.getgtokens()
    #print(p2hand, market, "p2 hand, market")
    move = RewardAgent.GenerateMove(p2hand, market, tokens)
    #print(move, "move")
    if move[0] == 0:
        p2movecheck = newGame.takegood(player, move[1])
    if move[0] == 1:
        p2movecheck = newGame.exchangegood(player, move[1])
    if move[0] == 2:
        p2movecheck = newGame.sell(player, move[1])
    if move[0] == 3:
        p2movecheck = newGame.takecamels(player)


    if not p2movecheck:
        print(p2movecheck, "move: ", move[0], "player: ", player, "arg: ", move[1], "hand: ", p2hand, "market: ", market)
        break
    #print(newGame.getscore(0))
    #print(newGame.getscore(1))


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