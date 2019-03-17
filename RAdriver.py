import RewardAgent


#hand = [0,1,3,1,0,0,3]
hand = [0,0,3,1,0,0,1]
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