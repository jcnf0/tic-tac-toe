# -*- coding: utf-8 -*-
import random
import numpy as np
from re import L
import tkinter as tk
import time
import copy

class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frameCan = tk.Frame(self)
        self.frameCan.pack(side='top')
        self.canvas = tk.Canvas(self.frameCan,width=600,height=480,bg='white')
        self.canvas.bind("<Button-1>",self.onClick_souris)
        self.canvas.pack()
        self.canvas.create_line(200,0,200,479)
        self.canvas.create_line(400,0,400,479)
        self.canvas.create_line(0,160,599,160)
        self.canvas.create_line(0,320,599,320)
        self.tictactoe = TicTacToe(self)
        self.frameButton = tk.Frame(self)
        self.frameButton.pack(side='bottom')
        self.listButton = []

        #Menu Button initialization
        menu_button_j1=tk.Menubutton(self.frameButton,text='Player 1')
        menu_button_j1.menu=tk.Menu(menu_button_j1)
        menu_button_j1["menu"]=menu_button_j1.menu
        menu_button_j1.menu.add_radiobutton(label='Human',command=lambda :self.tictactoe.change_player(0,'human'))
        menu_button_j1.menu.add_radiobutton(label='Random',command=lambda :self.tictactoe.change_player(0,'random'))
        menu_button_j1.menu.add_radiobutton(label='Best_First',command=lambda :self.tictactoe.change_player(0,'best_first'))
        menu_button_j1.menu.add_radiobutton(label='MinMax',command=lambda :self.tictactoe.change_player(0,'minmax'))   
        menu_button_j1.menu.add_radiobutton(label='AlphaBeta',command=lambda :self.tictactoe.change_player(0,'alphabeta'))      
        menu_button_j1.pack(side='left')

        menu_button_j2=tk.Menubutton(self.frameButton,text='Player 2')
        menu_button_j2.menu=tk.Menu(menu_button_j2)
        menu_button_j2["menu"]=menu_button_j2.menu
        menu_button_j2.menu.add_radiobutton(label='Human',command=lambda :self.tictactoe.change_player(1,'human'))
        menu_button_j2.menu.add_radiobutton(label='Random',command=lambda :self.tictactoe.change_player(1,'random'))
        menu_button_j2.menu.add_radiobutton(label='Best_First',command=lambda :self.tictactoe.change_player(1,'best_first'))        
        menu_button_j2.menu.add_radiobutton(label='MinMax',command=lambda :self.tictactoe.change_player(1,'minmax')) 
        menu_button_j2.menu.add_radiobutton(label='AlphaBeta',command=lambda :self.tictactoe.change_player(1,'alphabeta'))            
        menu_button_j2.pack(side='left')

        #Reset button initialization
        button_reset = tk.Button(self.frameButton, text='Reset', command = self.reset)
        button_reset.pack(side='left')

        #Quit button initialization
        button_exit = tk.Button(self.frameButton,text='Exit',command= lambda : self.destroy())
        button_exit.pack(side='left')

        self.listButton.append(menu_button_j1)
        self.listButton.append(menu_button_j2)
        self.listButton.append(button_exit)
        self.listButton.append(button_reset)

        self.liste_squares = []
        self.liste_squares_opposed = []
        #List of squares
        for j in range(3):
            for i in range(3):
                self.liste_squares.append([i*201,j*161,i*201+198,j*161+158])
                #To draw an X more easily
                self.liste_squares_opposed.append([i*201,j*161+159,i*201+199,j*161])

    #Method to reset the game
    def reset(self) :
        self.tictactoe=TicTacToe(self)
        self.tictactoe.repaint()

    def tracer(self,shape,square):
        #Draw the shape
        if shape=='o':
            self.canvas.create_oval(*(self.liste_squares[square]))
        else:
            self.canvas.create_line(*(self.liste_squares[square]))
            self.canvas.create_line(*(self.liste_squares_opposed[square]))
        self.update()
        
    def empty(self,square):
        #Empty the square
        self.canvas.create_rectangle(*(self.liste_squares[square]),fill='white',outline='white')
    
    def onClick_souris(self,event):
        x=event.x
        y=event.y
        #Square identification
        for square in self.liste_squares:
            if square[0]<x<square[2] and square[1]<y<square[3]:
                #Call the play function
                self.tictactoe.play(square_to_tuple(self.liste_squares.index(square)))

class TicTacToe():
    def __init__(self,interface):
        self.interface = interface
        self.matrix = np.full([3,3],None)
        self.played_moves=[[],[]]
        self.players = ['o','x']
        self.player_start = random.randint(0,1)
        self.player_now = self.player_start
        self.winner = None
        self.player_state = {0: 'human', 1: 'human'}
        self.possible_states=['human','random','best_first','minmax','alphabeta']
        self.depth_org=3

#---------------------------TICTACTOE ORGANIZATION---------------------------

    #Redraw the tictactoe on the interface
    def repaint(self):
        for i in range(3):
            for j in range(3):
                self.interface.empty(tuple_to_square(i,j))
                if self.matrix[i,j] == 'x':
                    self.interface.tracer('x', tuple_to_square(i,j))
                elif self.matrix[i,j] == 'o' :
                    self.interface.tracer('o', tuple_to_square(i,j))

    #Method handling moves
    def play(self,move_if_human):
        #If the player is a human, we use the move in argument
        if self.player_state[self.player_now]=='human' and self.matrix[move_if_human]==None and self.winner==None:
            #Play of the move then refresh the game
            self.matrix[move_if_human]=self.players[self.player_now]
            self.played_moves[self.player_now].append(move_if_human)
            self.repaint()
            self.test_winner()
            self.player_now=other_player(self.player_now)
            
        #Loop on the AI
        while self.winner==None and self.player_state[self.player_now]!='human':
            #Move generation depending on the AI
            move=self.place_move_ia()
            if move!=None:
                self.matrix[move]=self.players[self.player_now]
                self.played_moves[self.player_now].append(move)
                self.repaint()
            else:
                break
            #Game refresh
            self.test_winner()
            if self.winner==None:
                self.player_now=other_player(self.player_now)

    #Returns a move corresponding to the AI
    def place_move_ia(self):
        move=None
        if self.player_state[self.player_now]=='random':
            move=self.move_random()
        elif self.player_state[self.player_now]=='best_first':
            move=self.move_best_first()

        elif self.player_state[self.player_now]=='minmax':
            move=self.move_min_max()

        elif self.player_state[self.player_now]=='alphabeta':
            move=self.move_min_max_alpha_beta()

        if move==None:
            print('No move found')
            return None
        #Forbidden move
        if self.matrix[move]!=None:
            print('Move on ({},{}) forbidden!'.format(move[0],move[1]))
            return None
        else:
            return move

    #Test whether there is a winner or not
    def test_winner(self):
        D1=self.matrix.diagonal()
        D2=np.fliplr(self.matrix).diagonal()
        for k in range(3):
            Lk=self.matrix[k]
            Ck=self.matrix[:,k]
            if (Lk==self.players[self.player_now]).sum()==3 or (Ck==self.players[self.player_now]).sum()==3:
                self.winner='Player {}'.format(self.player_now+1)
                break
        if (D1==self.players[self.player_now]).sum()==3 or (D2==self.players[self.player_now]).sum()==3:
            self.winner='Player {}'.format(self.player_now+1)
        
        if self.winner!=None:
            print('Winner : {}'.format(self.winner))
            return self.winner
        
        if None not in self.matrix:
            #Draw
            self.winner='Draw'
        return self.winner

    #Change the state of players (human,random,best_first,...)
    def change_player(self,player,new_state):
        #Test is new state is possible
        if new_state in self.possible_states:
            self.player_state[player]=new_state
        print("PLAYER STATE : ", self.player_state)

#---------------------------IA ALEATOIRE---------------------------
    #Random move
    def move_random(self):
        squares_libres=[]
        #Add all free squares
        for i in range(3):
            for j in range(3):
                if self.matrix[i,j]==None:
                    squares_libres.append(i*3+j)
        #Random choice
        return square_to_tuple(random.choice(squares_libres))

#---------------------------IA BEST FIRST---------------------------
    #Best First move
    def move_best_first(self):
        moves_libres=[]
        Eval=[]
        #Add all free squares
        for i in range(3):
            for j in range(3):
                if self.matrix[i,j]==None:
                    moves_libres.append((i,j))
        #Evaluation calculation
        for (i,j) in moves_libres:
            Eval.append(self.evaluation(self.player_now,i,j))
        #Take the move with the best evaluation
        (i,j)=moves_libres[Eval.index(max(Eval))]
        return (i,j)

    #Gives the evaluation of a move
    def evaluation(self,player,i,j,deg=2):
        Diags=[(0,0),(1,1),(2,2),(2,0),(0,2)]
        NL1=1
        NL2=0
        NC1=1
        NC2=0
        ND1=0
        ND2=0
        #Diagonals
        if (i,j) in Diags:
            for (x,y) in Diags:
                if self.matrix[x,y]=='o' and player==0:
                    ND1+=1
                elif self.matrix[x,y]=='x' and player==1:
                    ND2+=1
        for k in range(2):
            #Rows
            if self.matrix[i,(j+k)%3]=='o' and player==0:
                NL1+=1
            elif self.matrix[i,(j+k)%3]=='x' and player==1:
                NL2+=1

            #Columns
            if self.matrix[(i+k)%3,j]=='o' and player==0:
                NC1+=1
            elif self.matrix[i,(j+k)%3]=='x' and player==1:
                NC2+=1
        #Deg=2 to have a quadratic function (arbitrary choice)
        return (NL1-NL2)**deg+(NC1-NC2)**deg+(ND1-ND2)**deg   

#---------------------------MINMAX AI---------------------------
    #MinMax move
    def move_min_max(self):
        mode='max'
        if self.depth_org<=0 or self.depth_org>6:
            raise ValueError('Impossible depth')
        board_to_play,valeur=self.min_max(self.matrix,self.depth_org,mode,self.player_now)
        #Get the move to play
        for i in range(3):
            for j in range(3):
                if board_to_play[i,j]!=self.matrix[i,j]:
                    return (i,j)
        return None

    #MinMax algorithm
    def min_max(self,board,depth,mode,player):
        #Test if board is empty
        if any(x in board for x in self.players):
            if self.win_board_minmax(board,other_player(player)) or depth==0 or None not in board:
                return (board,self.score_board_minmax(board,other_player(player),change_mode(mode)))
        min_score=np.inf
        max_score=-np.inf
        best_board=board
        if mode=='max':
            best_score=max_score
        else:
            best_score=min_score

        #Case distinction to know if we need to add a move or to make a permutation 
        if not self.win_board_minmax(board,player):
            liste_boardx_succ=self.succ_board_not_won(board,player)
        else:
            liste_boardx_succ=self.succ_board_won(board,player)

        for board_bis in liste_boardx_succ:
            board1, score=self.min_max(board_bis,depth-1,change_mode(mode),other_player(player))
            #Case distinction depending on the current player
            if mode=='max':
                #Maximization (the AI plays)
                if score>max_score:
                    best_score=score
                    best_board=board1
                    max_score=best_score
            else:
                #Minimization (the other player plays)
                if score<min_score:
                    best_score=score
                    best_board=board1
                    min_score=best_score
        if depth==self.depth_org:
            return best_board,best_score
        else:
            return board, best_score

    #Additional methods for the MinMax

    #Generate other boards by permutation
    def succ_board_won(self,board,player):
        L=[]
        #No need to deep copy because we only permute elements
        board_succ=np.copy(board)
        for (i1,j1) in [(k,l) for k in range(3) for l in range(3)]:
            for (i2,j2) in [(k,l) for k in range(3) for l in range(3)]:
                if board[i1,j1]==self.players[player] and board[i2,j2] is None:
                    board_succ[i1,j1],board_succ[i2,j2]=board_succ[i2,j2],board_succ[i1,j1]
                    L.append(board_succ)
                    board_succ=np.copy(board)
        return L

    #Generate next boards by adding a move
    def succ_board_not_won(self,board,player):
        L=[]
        board_succ=copy.deepcopy(board)
        for i in range(3):
            for j in range(3):
                if board[i,j] is None:
                    board_succ[i,j]=self.players[player]
                    L.append(board_succ)
                    board_succ=copy.deepcopy(board)
        return L

    #Test if a player won in the board
    def win_board_minmax(self,board,player):
        D1=board.diagonal()
        D2=np.fliplr(board).diagonal()        
        for k in range(3):
            Lk=board[k]
            Ck=board[:,k]
            if (Lk==self.players[player]).sum()==3:
                return True
            if (Ck==self.players[player]).sum()==3:
                return True
        if (D1==self.players[player]).sum()==3:
            return True
        if (D2==self.players[player]).sum()==3:
            return True 
        return False

    #Gives a score to a board
    def score_board_minmax(self,board,player,mode):
        #blockX gives the squares that prevent X ways of winning
        block2=[(0,1),(1,0),(2,1),(1,2)]
        block3=[(0,0),(0,2),(2,0),(2,2)]
        block4=[(1,1)]
        blocked_sum1=0
        blocked_sum2=0

        #If AI wins
        if (self.win_board_minmax(board,player) and mode=='max') or (self.win_board_minmax(board,other_player(player)) and mode=='min'):
            return np.inf
        
        #If the other player wins
        if (self.win_board_minmax(board,player) and mode=='min') or (self.win_board_minmax(board,other_player(player)) and mode=='max'):
            return -np.inf
        #Equality
        if None not in board:
            return 0

        for (i,j) in block2:
            if board[i,j]==self.players[player]:
                blocked_sum1+=2
            elif board[i,j]==self.players[other_player(player)]:
                blocked_sum2-=2
                
        for (i,j) in block3:
            if board[i,j]==self.players[player]:
                blocked_sum1+=3
            elif board[i,j]==self.players[other_player(player)]:
                blocked_sum2-=3
                      
        for (i,j) in block4:
            if board[i,j]==self.players[player]:
                blocked_sum1+=4
            elif board[i,j]==self.players[other_player(player)]:
                blocked_sum2-=4

        #Case disctinction to get the correct players order
        if mode=='max':
            return (8-blocked_sum2)-(8-blocked_sum1)
        else:
            return (8-blocked_sum1)-(8-blocked_sum2)

#---------------------------ALPHA BETA---------------------------

    def move_min_max_alpha_beta(self):
        mode='max'
        if self.depth_org<=0 or self.depth_org>6:
            raise ValueError('Impossible depth')
        #Alpha and Beta initialization
        alpha=-np.inf
        beta=np.inf
        board_to_play,valeur=self.min_max_alpha_beta(self.matrix,self.depth_org,alpha,beta,mode,self.player_now)
        for i in range(3):
            for j in range(3):
                if board_to_play[i,j]!=self.matrix[i,j]:
                    return (i,j)
        return None

    def min_max_alpha_beta(self,board,depth,alpha,beta,mode,player):
        if any(x in board for x in self.players):
            if self.win_board_minmax(board,other_player(player)) or depth==0 or None not in board:
                return (board,self.score_board_minmax(board,other_player(player),change_mode(mode)))
        min_score=np.inf
        max_score=-np.inf
        best_board=board
        if mode=='max':
            best_score=max_score
        else:
            best_score=min_score

        if not self.win_board_minmax(board,player):
            liste_boardx_succ=self.succ_board_not_won(board,player)
        else:
            liste_boardx_succ=self.succ_board_won(board,player)

        for board_bis in liste_boardx_succ:
            board1, score=self.min_max_alpha_beta(board_bis,depth-1,alpha,beta,change_mode(mode),other_player(player))
            if mode=='max':
                if score>max_score:
                    best_score=score
                    best_board=board1
                    max_score=best_score
                    alpha=max(best_score,alpha)
            else:
                if score<min_score:
                    best_score=score
                    best_board=board1
                    min_score=best_score
                    beta=min(best_score,beta)
            #Don't consider the branch if alpha>=beta
            if alpha>=beta:
                break
        if depth==self.depth_org:
            return best_board,best_score
        else:
            return board, best_score

#---------------------------UTILITARY FUNCTIONS---------------------------

#Function allowing the bijection between the number of the square and the tuple associated
def tuple_to_square(i,j):
    return i*3+j
def square_to_tuple(square):
    return (square//3,square%3)

#Function used in the MinMax
def change_mode(mode):
    if mode=='min':
        return 'max'
    elif mode=='max':
        return 'min'
    else:
        return None

#Function to swap player
def other_player(player):
    return (player+1)%2

if __name__ == "__main__" :
    game = Interface()
    game.mainloop()
