# 在这里实现MyGO Agent
# 2025.3.14@Zhuiri Xiao
# 使用QLearning算法实现

import random
import sys, json
from read import readInput
from write import writeOutput
from host import GO
import numpy

def state2str(state):
    return ''.join([str(state[i][j]) for i in range(5) for j in range(5)])


class Qlearner():
    def __init__(self, default_value=0,alpha=0.6,beta=0.9):
        self.type = 'Qlearner' #agent的策略名称
        self.chess_color=None
        
        
        self.qvalues={}
        self.state_history_sequence=[]

        self.init_value=default_value #初始化价值,初始时候默认下在每一个位置价值都是0,价值的范围是[-1,1]
        self.win_bonus=1.0
        self.lose_bonus=-1.0
        self.draw_bonus=0.0
        
        self.alpha=alpha
        self.beta=beta

    def set_color(self, player_color):
        #player_color: 1('X') or 2('O').
        self.chess_color=player_color
        # 平局一般应该奖励后手
        if self.chess_color==1:
            self.draw_bonus=0.0-0.2
        else:
            self.draw_bonus=0.0+0.3


    def get_q_table(self,board_state):
        # 如果历史Q记录里面没有当前局面,那么返回默认值
        return self.q_values.setdefault(
            board_state,
            [[self.initial_value] * 5 for _ in range(5)]
        )



    def q_reflective_learning(self,winner): 
        """
            每下完一盘棋就开始反思和学习过往每一步的价值Qvalues
        """
        if winner==0:
            bonus=self.draw_bonus
        elif winner==self.chess_color:
            bonus=self.win_bonus
        else:
            bonus=self.lose_bonus

        states_memory=self.state_history_sequence.reverse() #从最近的棋谱开始学习
        qmax=float('-inf')
        for chess_record in states_memory:
            board_state, move=chess_record

            q_table=self.get_q_table(board_state=board_state)
            if qmax<-1: # 小于-1说明不在范围之内是第一次更新qtable
                q_table[move]=bonus
                
            else:
                current_q=q_table[move]
                q_table[move]=round(qmax*self.beta*(1-self.alpha)+current_q*(1-self.alpha),6)
                
            qmax=numpy.max(q_table)

        self.state_history_sequence=[] #学习完成清空记忆
      
    def save(self):
        with open('qtable.json', 'w') as json_file:
            json.dump(self.qvalues, json_file)

    def Q_Move(self, go, piece_type):
        '''
        Get one input.
        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))

        if not possible_placements:
            return "PASS"
        
        state_str=state2str(go.board)
        qtable=self.get_q_table(state_str)
        current_max_value=float('-inf')
        while True:
            row,col=self._get_max_index(qtable=qtable)
            go.verbose=True # 输出冗余调试信息
            if go.valid_place_check(row,col,piece_type,test_check=True):
                self.state_history_sequence.append(state2str,(row,col))
                return (row,col)
            else:
                qtable[(row,col)]=float('-inf')

        return random.choice(possible_placements)
    def _get_max_index(self,qtable):
        maxv=float('-inf')
        resp=(0,0)
        for i in range(5):
            for j in range(5):
                if qtable[(i,j)]>maxv:
                    maxv=qtable
                    resp=(i,j)
        return resp
    
if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = Qlearner()
    action = player.Q_Move(go, piece_type)
    writeOutput(action)