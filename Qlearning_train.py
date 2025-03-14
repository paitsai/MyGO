
import sys
import time
from pathlib import Path
from host import GO
from random_player import RandomPlayer
from my_player import MyPlayer

PLAYER_X = 1
PLAYER_O = 2

def battle(player1, player2, iter,mode=PLAYER_X):
    win = 0
    lose = 0
    tie = 0
    player1.set_side(mode)
    start = time.time()
    for i in range(0, iter):
        if(i % 100 == 0):
            print(time.time() - start)
            start = time.time()
            print("---battle ", i, "---", i/iter*100, '%')
        go = GO(5)
        #go.verbose = True
        result = go.play(player1, player2, True)
        if result == 0:
            tie+=1
        elif result == 1:
            win+=1
        else:
            lose+=1
        player1.learn(result)
    
    
    print("win: ", win)
    print("lose: ", lose)
    print("tie: ", tie)

if __name__ == "__main__":

    start = time.time()
    print("开始创建")
    my_player = MyPlayer()
    player_1 = RandomPlayer()
    player_2 = RandomPlayer()
    print(time.time() - start)
    print("玩家创建完毕")
    NUM = 10
    battle(my_player, player_2, NUM,mode=PLAYER_X)
    battle(player_1, my_player, NUM,mode=PLAYER_O)
    my_player.save()
    
    