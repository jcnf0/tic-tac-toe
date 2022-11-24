# -*- coding: utf-8 -*-
"""
Code pour la version Ultimate du tictactoe
"""
import random
import numpy as np
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
        self.next_tictactoe=None
        self.winner_global=None

        #TIC TAC TOE PARAMETERS CENTRALIZATION
        self.players_moves=[[],[]]
        self.players = ['o','x']
        self.start_player = random.randint(0,1)
        self.current_player = self.start_player
        self.player_state = {0: 'human', 1: 'human'}
        self.possible_states=['human','random','best_first','minmax','alphabeta']

        w=600
        h=480
        pas_x=600//9
        pas_y=480//9
        for k in range(9):
            self.canvas.create_line(k*pas_x,0,k*pas_x,h-1,width=3//(1+k%3))
            self.canvas.create_line(0,k*pas_y,w-1,k*pas_y,width=3//(1+k%3))
        self.tictactoe= [TicTacToe(self,id_tictactoe=k) for k in range(9)]

        #BUTTONS
        self.frameButton = tk.Frame(self)
        self.frameButton.pack(side='bottom')

        self.listButton = []
        menu_button_j1=tk.Menubutton(self.frameButton,text='Player 1')
        menu_button_j1.menu=tk.Menu(menu_button_j1)
        menu_button_j1["menu"]=menu_button_j1.menu
        menu_button_j1.menu.add_radiobutton(label='Human',command=lambda :self.change_player(0,'human'))
        menu_button_j1.menu.add_radiobutton(label='Random',command=lambda :self.change_player(0,'random'))
        menu_button_j1.menu.add_radiobutton(label='Best_First',command=lambda :self.change_player(0,'best_first'))
        menu_button_j1.menu.add_radiobutton(label='MinMax',command=lambda :self.change_player(0,'minmax'))  
        menu_button_j1.menu.add_radiobutton(label='AlphaBeta',command=lambda :self.change_player(0,'alphabeta'))        
        menu_button_j1.pack(side='left')

        menu_button_j2=tk.Menubutton(self.frameButton,text='Player 2')
        menu_button_j2.menu=tk.Menu(menu_button_j2)
        menu_button_j2["menu"]=menu_button_j2.menu
        menu_button_j2.menu.add_radiobutton(label='Human',command=lambda :self.change_player(1,'human'))
        menu_button_j2.menu.add_radiobutton(label='Random',command=lambda :self.change_player(1,'random'))
        menu_button_j2.menu.add_radiobutton(label='Best_First',command=lambda :self.change_player(1,'best_first'))        
        menu_button_j2.menu.add_radiobutton(label='MinMax',command=lambda :self.change_player(1,'minmax'))   
        menu_button_j2.menu.add_radiobutton(label='AlphaBeta',command=lambda :self.change_player(1,'alphabeta'))            
        menu_button_j2.pack(side='left')


        button_reset = tk.Button(self.frameButton, text='Reset', command = self.reset)
        button_reset.pack(side='left')

        button_exit = tk.Button(self.frameButton,text='Exit',command= lambda : self.destroy())
        button_exit.pack(side='left')

        self.listButton.append(menu_button_j1)
        self.listButton.append(menu_button_j2)
        self.listButton.append(button_exit)
        self.listButton.append(button_reset)

        self.list_squares = []
        self.list_squares_opposed = []
        #List of squares
        for j in range(9):
            for i in range(9):
                self.list_squares.append([i*pas_x+1,j*pas_y+2,i*pas_x+1+pas_x-2,j*pas_y-1+pas_y])
                #To draw an X more easily
                self.list_squares_opposed.append([i*pas_x+1,j*pas_y+1+pas_y-1,i*pas_x+1+pas_x-1,j*pas_y+1])
        
        self.list_squares_primitive = []
        self.list_squares_opposed_primitive = []
        for j in range(3):
            for i in range(3):
                self.list_squares_primitive.append([i*201,j*161,i*201+198,j*161+158])
                #To draw an X more easily
                self.list_squares_opposed_primitive.append([i*201,j*161+159,i*201+199,j*161])


    def change_player(self,player,new_state):
        if new_state in self.possible_states:
            self.player_state[player]=new_state
        print("PLAYER STATE : ", self.player_state)

    #Method to reset the game
    def reset(self) :
        self.tictactoe=[TicTacToe(self,id_tictactoe=k) for k in range(9)]
        w=600
        h=480
        pas_x=w//9
        pas_y=h//9
        self.canvas.create_rectangle([0,0,600,480],fill='white',outline='white')
        for k in range(9):
            self.canvas.create_line(k*pas_x,0,k*pas_x,h-1,width=3//(1+k%3))
            self.canvas.create_line(0,k*pas_y,w-1,k*pas_y,width=3//(1+k%3))
        self.next_tictactoe=None
        self.players_moves=[[],[]]
        self.players = ['o','x']
        self.start_player = random.randint(0,1)
        self.current_player = self.start_player
        self.winner_global=None

    #Draw the symbols in the sub-tictactoe 
    def draw(self,forme,square):
        if forme=='o':
            self.canvas.create_oval(*(self.list_squares[square]))
        else:
            self.canvas.create_line(*(self.list_squares[square]))
            self.canvas.create_line(*(self.list_squares_opposed[square]))
        self.update()

    #Draw on the global tictactoe        
    def draw_general(self,forme,id_tictactoe):
        self.canvas.create_rectangle(*(self.list_squares_primitive[id_tictactoe]),fill='white',outline='white')
        if forme=='o':
            self.canvas.create_oval(*(self.list_squares_primitive[id_tictactoe]))
        else:
            self.canvas.create_line(*(self.list_squares_primitive[id_tictactoe]))
            self.canvas.create_line(*(self.list_squares_opposed_primitive[id_tictactoe]))
        self.draw_lines()

    #Draw the thick lines
    def draw_lines(self):
        w=600
        h=480
        pas_x=w//9
        pas_y=h//9
        for k in [0,3,6]:
            self.canvas.create_line(k*pas_x,0,k*pas_x,h-1,width=3)
            self.canvas.create_line(0,k*pas_y,w-1,k*pas_y,width=3)

    #Draw the big shapes
    def global_drawing(self):
        for k in range(9):
            if self.tictactoe[k].winner=='Player 1':
                self.draw_general(self.players[0],k)
            elif self.tictactoe[k].winner=='Player 2':
                self.draw_general(self.players[1],k)

    def empty(self,square):
        #Empty the square
        self.canvas.create_rectangle(*(self.list_squares[square]),fill='white',outline='white')
    
    def onClick_souris(self,event):
        x=event.x
        y=event.y
        for square in self.list_squares:
            if square[0]<x<square[2] and square[1]<y<square[3]:
                id_square=self.list_squares.index(square)
                if (self.next_tictactoe is None or square_to_id_tictactoe(id_square)==self.next_tictactoe) and self.winner_global==None:
                    move=square_to_tuple(id_square)
                    self.play(move,square_to_id_tictactoe(id_square))

    #Method allowing to play
    def play(self,move_si_human,id_tictactoe):
        if self.next_tictactoe is not None:
            if None not in self.tictactoe[self.next_tictactoe].matrix:
                self.global_drawing()
                return None
        if self.next_tictactoe is None or self.next_tictactoe==id_tictactoe:
            if self.player_state[self.current_player]=='human':
                self.tictactoe[id_tictactoe].play_move(move_si_human)
            else:
                first_tictactoe_random=random.randint(0,8)
                move=self.tictactoe[first_tictactoe_random].play_move_ia()
                self.tictactoe[first_tictactoe_random].play_move(move)
        
        while self.player_state[self.current_player]!='human' and self.winner_global==None:
            move=self.tictactoe[self.next_tictactoe].play_move_ia()
            if move==None:
                self.next_tictactoe=(self.next_tictactoe+1)%9
                break
            self.tictactoe[self.next_tictactoe].play_move(move)
        return None

    #Test if a player won in the global tictactoe
    def test_winner_general(self):
        list_winners=[self.tictactoe[k].winner for k in range(9)]
        D1=[list_winners[0],list_winners[4],list_winners[8]]
        D2=[list_winners[2],list_winners[4],[list_winners[6]]]
        if self.winner_global==None:
            for k in range(3):
                Lk=list_winners[3*k:3*k+3]
                Ck=[list_winners[k+3*i] for i in range(3)]
                if sum(1 for a in Lk if a=='Player {}'.format(self.current_player+1))==3 or sum(1 for a in Ck if a=='Player {}'.format(self.current_player+1))==3:
                    self.winner_global='Player {}'.format(self.current_player+1)
                    break
            if sum(1 for a in D1 if a=='Player {}'.format(self.current_player+1))==3 or sum(1 for a in D2 if a=='Player {}'.format(self.current_player+1))==3:
                self.winner_global='Player {}'.format(self.current_player+1)
            
            if self.winner_global!=None:
                print('Winner global : {}'.format(self.winner_global))
                self.global_drawing()
            
            if None not in list_winners:
                #Draw
                self.winner_global='Draw'
                print('Draw')
        return self.winner_global      


class TicTacToe():
    def __init__(self,interface,id_tictactoe=0):
        self.interface = interface
        self.id=id_tictactoe
        self.matrix = np.full([3,3],None)
        self.winner = None
        self.depth_org=3

#---------------------------TICTACTOE ORGANIZATION---------------------------

#Redraw the tictactoe on the interface
    def repaint(self):
        for i in range(3):
            for j in range(3):
                self.interface.empty(tuple_to_square(i,j,id_tictactoe=self.id))
                if self.matrix[i,j] == 'x':
                    self.interface.draw('x', tuple_to_square(i,j,id_tictactoe=self.id))
                elif self.matrix[i,j] == 'o' :
                    self.interface.draw('o', tuple_to_square(i,j,id_tictactoe=self.id))
        self.interface.draw_lines()

    #Method handling moves in a sub-tictactoe
    def play_move(self,move):
        if self.matrix[move] is None and (self.interface.next_tictactoe==self.id or self.interface.next_tictactoe is None):
            self.matrix[move]=self.interface.players[self.interface.current_player]
            self.interface.players_moves[self.interface.current_player].append([self.id,move])
            self.test_winner()
            self.repaint()
            self.interface.test_winner_general()
            self.interface.next_tictactoe=move[0]*3+move[1]
            self.interface.current_player=autre_player(self.interface.current_player)

        if None not in self.matrix:
            if self.winner=='Player 1':
                self.interface.draw_general(self.interface.players[0],self.id)
            elif self.winner=='Player 2':
                self.interface.draw_general(self.interface.players[1],self.id)

    #Returns a move corresponding to the AI
    def play_move_ia(self):
        move=None
        if self.interface.player_state[self.interface.current_player]=='random':
            move=self.move_random()

        elif self.interface.player_state[self.interface.current_player]=='best_first':
            move=self.move_best_first()

        elif self.interface.player_state[self.interface.current_player]=='minmax':
            move=self.move_min_max()

        elif self.interface.player_state[self.interface.current_player]=='alphabeta':
            move=self.move_min_max_alpha_beta()

        if move==None:
            print('No move found')
            return None
        if self.matrix[move]!=None:
            print('Coup on ({},{}) forbidden!'.format(move[0],move[1]))
            return None
        else:
            return move

    def test_winner(self):
        D1=self.matrix.diagonal()
        D2=np.fliplr(self.matrix).diagonal()
        if self.winner==None:
            for k in range(3):
                Lk=self.matrix[k]
                Ck=self.matrix[:,k]
                if (Lk==self.interface.players[self.interface.current_player]).sum()==3 or (Ck==self.interface.players[self.interface.current_player]).sum()==3:
                    self.winner='Player {}'.format(self.interface.current_player+1)
                    break
            if (D1==self.interface.players[self.interface.current_player]).sum()==3 or (D2==self.interface.players[self.interface.current_player]).sum()==3:
                self.winner='Player {}'.format(self.interface.current_player+1)
            
            if self.winner!=None:
                print('Winner of TicTacToe {} : {}'.format(self.id,self.winner))
            
            if None not in self.matrix:
                #Draw
                self.winner='Draw'
                print('Draw')
        return self.winner

#---------------------------RANDOM AI---------------------------
    def move_random(self):
        squares_libres=[]
        for i in range(3):
            for j in range(3):
                if self.matrix[i,j]==None:
                    squares_libres.append(i*3+j)
        if squares_libres==[]:
            return None
        move=random.choice(squares_libres)
        return (move//3,move%3)

#---------------------------BEST FIRST AI---------------------------
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
            Eval.append(self.evaluation(self.interface.current_player,i,j))
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
            raise ValueError('Profondeur impossible')
        board_to_play,valeur=self.min_max(self.matrix,self.depth_org,mode,self.interface.current_player)
        #Get the move to play
        for i in range(3):
            for j in range(3):
                if board_to_play[i,j]!=self.matrix[i,j]:
                    return (i,j)
        return None

    #MinMax algorithm
    def min_max(self,board,depth,mode,player):
        #Test if board is empty
        if any(x in board for x in self.interface.players):
            if self.gagne_board_minmax(board,autre_player(player)) or depth==0 or None not in board:
                return (board,self.score_board_minmax(board,autre_player(player),change_mode(mode)))
        min_score=np.inf
        max_score=-np.inf
        best_board=board
        if mode=='max':
            best_score=max_score
        else:
            best_score=min_score

        #Case distinction to know if we need to add a move or to make a permutation 
        if not self.gagne_board_minmax(board,player):
            list_boardx_succ=self.succ_board_not_won(board,player)
        else:
            list_boardx_succ=self.succ_board_won(board,player)

        for board_bis in list_boardx_succ:
            board1, score=self.min_max(board_bis,depth-1,change_mode(mode),autre_player(player))
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
                if board[i1,j1]==self.interface.players[player] and board[i2,j2] is None:
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
                    board_succ[i,j]=self.interface.players[player]
                    L.append(board_succ)
                    board_succ=copy.deepcopy(board)
        return L

    #Test if a player won in the board
    def gagne_board_minmax(self,board,player):
        D1=board.diagonal()
        D2=np.fliplr(board).diagonal()        
        for k in range(3):
            Lk=board[k]
            Ck=board[:,k]
            if (Lk==self.interface.players[player]).sum()==3:
                return True
            if (Ck==self.interface.players[player]).sum()==3:
                return True
        if (D1==self.interface.players[player]).sum()==3:
            return True
        if (D2==self.interface.players[player]).sum()==3:
            return True 
        return False

    #Gives a score to a board
    def score_board_minmax(self,board,player,mode):
        #blockX gives the squares that prevent X ways of winning
        bloque2=[(0,1),(1,0),(2,1),(1,2)]
        bloque3=[(0,0),(0,2),(2,0),(2,2)]
        bloque4=[(1,1)]
        somme_bloques1=0
        somme_bloques2=0

        #If AI wins
        if (self.gagne_board_minmax(board,player) and mode=='max') or (self.gagne_board_minmax(board,autre_player(player)) and mode=='min'):
            return np.inf
        
        #If the other player wins
        if (self.gagne_board_minmax(board,player) and mode=='min') or (self.gagne_board_minmax(board,autre_player(player)) and mode=='max'):
            return -np.inf
        #Equality
        if None not in board:
            return 0

        for (i,j) in bloque2:
            if board[i,j]==self.interface.players[player]:
                somme_bloques1+=2
            elif board[i,j]==self.interface.players[autre_player(player)]:
                somme_bloques2-=2

        for (i,j) in bloque3:
            if board[i,j]==self.interface.players[player]:
                somme_bloques1+=3
            elif board[i,j]==self.interface.players[autre_player(player)]:
                somme_bloques2-=3
                    
        for (i,j) in bloque4:
            if board[i,j]==self.interface.players[player]:
                somme_bloques1+=4
            elif board[i,j]==self.interface.players[autre_player(player)]:
                somme_bloques2-=4

        #Case disctinction to get the correct players order
        if mode=='max':
            return (8-somme_bloques2)-(8-somme_bloques1)
        else:
            return (8-somme_bloques1)-(8-somme_bloques2)

#---------------------------ALPHA BETA---------------------------
    def move_min_max_alpha_beta(self):
        mode='max'
        if self.depth_org<=0 or self.depth_org>6:
            raise ValueError('Impossible depth')
        #Alpha and Beta initialization
        alpha=-np.inf
        beta=np.inf
        board_to_play,valeur=self.min_max_alpha_beta(self.matrix,self.depth_org,alpha,beta,mode,self.interface.current_player)
        for i in range(3):
            for j in range(3):
                if board_to_play[i,j]!=self.matrix[i,j]:
                    return (i,j)
        return None

    def min_max_alpha_beta(self,board,depth,alpha,beta,mode,player):
        if any(x in board for x in self.interface.players):
            if self.gagne_board_minmax(board,autre_player(player)) or depth==0 or None not in board:
                return (board,self.score_board_minmax(board,autre_player(player),change_mode(mode)))
        min_score=np.inf
        max_score=-np.inf
        best_board=board
        if mode=='max':
            best_score=max_score
        else:
            best_score=min_score

        if not self.gagne_board_minmax(board,player):
            list_boardx_succ=self.succ_board_not_won(board,player)
        else:
            list_boardx_succ=self.succ_board_won(board,player)

        for board_bis in list_boardx_succ:
            board1, score=self.min_max_alpha_beta(board_bis,depth-1,alpha,beta,change_mode(mode),autre_player(player))
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
#Bijection between tuple and int to represent a square of a sub-tictactoe using its ID
def tuple_to_square(i,j,id_tictactoe=0):
    m,n=id_tictactoe_to_tuple(id_tictactoe)
    return (i+3*m)*9+(j+3*n)

#Bijection int tuple between the ID of the sub-tictactoe and its position in the global tictactoe
def id_tictactoe_to_tuple(id_tictactoe):
    return (id_tictactoe//3,id_tictactoe%3)

#Bijection int tuple to represent the square in a sub-tictactoe
def square_to_tuple(square):
    i=(square//9)%3
    j=square%3
    return (i,j)

#Injection to get the ID of a sub-tictactoe associated to a square
def square_to_id_tictactoe(square):
    i=(square//9)//3
    j=(square%9)//3
    return i*3+j

#Function used in the MinMax
def change_mode(mode):
    if mode=='min':
        return 'max'
    elif mode=='max':
        return 'min'
    else:
        return None

#Function to swap player
def autre_player(player):
    return (player+1)%2

if __name__ == "__main__" :
    game = Interface()
    game.mainloop()
