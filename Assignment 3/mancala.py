
import sys
import os
from time import time
from io import StringIO

#Varialbes for mancala pit and depth
#each player has 7 pits, 6 small ones, one Mancala pit (to score)
MANCALA_PIT = 7
DEPTH = 5

#defining the class to represent the board
class Board:

    #some self representation functions
    def __str__(self, *args, kwargs):
        return str(self.board)

    def __repr__(self, *args, **kwargs):
        return "Board%s" % self.__str__()

    #defining property class to modify self object (setting points for player 1 and player 2)
    @property
    def player1_points(self):
        if self.no_moves_remaining():
            return sum(self.board[1:8])
        else:
            return self.board[7]

    @property
    def player2_points(self):
        if self.no_moves_remaining():
            return self.board[0] + sum(self.board[8:])
        else:
            return self.board[0]    
    #the above functions are defined to make it easier to print, and update the board as moves are made
    
    
    #initializing the board

    def __init__(self, board=None):
        self.go_again = False
        if board is not None:
            self.board = board.board[:]
            self.reversed = board.reversed
        else:
            self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
            self.reversed = False            

    #define a function to check if moves can be made
    def no_moves_remaining(self):
        if any(self.board[8:]) == False or any(self.board[1:7]) == False:
            return True
        return False

    #define this function to find all possible moves given the current board state.
    #this function will help you determine the best possible move when using min_max 
    #and alpha_beta.
    def find_moves(self):
        moves = []
        if self.reversed: #for player two check index 8-13
            for i in range(8, 14):
                if self.board[i] > 0:
                    moves.append(i)
        else:
            for i in range(1, 7): #for player1 check index 1-6
                if self.board[i] > 0:
                    moves.append(i)
        return moves

    #definie the "update_board()" function here.
    #this function updates the board using the parameter "n" passed to it.
    #using "n" as the players pit location, take the stones from that location,
    #and update the board according to the rules (counterclockwise).
    #if helper functions are needed, use the space above to define them.
    def update_board(self, n):
       # print("in update_board")
        num = self.board[n]    #store nth pit value and set it to zero
        self.board[n] = 0
        cur_pit = n
        #loop for the number that was removed from the pit
        for i in range(0, num):
            cur_pit += 1
            if cur_pit > 13:
                cur_pit = 0
            #if cur_pit == 0 and its player1s turn we skip player2s mancala 
            if cur_pit == 0 and self.reversed == False:
                cur_pit += 1
            #if cur_pit == 7 and its player2s turn we skip player1s mancala  
            if cur_pit == 7 and self.reversed == True:
                cur_pit += 1
            self.board[cur_pit] += 1
        #check if last pit was empty and on players side
        #if true pit on other side goes to current players mancala
        if self.reversed and cur_pit > 7:
            if self.board[cur_pit] == 1:
                self.board[cur_pit] = 0
                num = self.board[14 - cur_pit]
                self.board[14 - cur_pit] = 0
                self.board[0] += num
                self.board[0] += 1
        #if its player1s turn, check if last stone was placed in empty pit
        #on their side
        if not(self.reversed) and 0 < cur_pit and cur_pit <= 6: 
            if self.board[cur_pit] == 1:
                self.board[cur_pit] = 0
                num = self.board[14 - cur_pit]
                self.board[14 - cur_pit] = 0
                self.board[7] += num
                self.board[7] += 1
        #if end in mancala player goes again
        if cur_pit == 0 or cur_pit == 7:
            self.go_again = True

        
    #define the min_max function below
    #the starter code defines it with self and depth=3. 
    #Add additional parameters if necessary
    def min_max(self, depth=3):
        # if we reach depth or no moves remaining, return heuristic
        if depth == 0 or self.no_moves_remaining():
            return self.calculate_heurestic_score()
        v = 0
        new_depth = depth - 1
        # if player1s turn we do max node
        if not(self.reversed):
            v = -999
            for i in self.find_moves(): #loop through potential moves
                copy = Board(self)
                copy.update_board(i)
                if not(copy.go_again): #if player goes agian we don't update turn flag
                    copy.reversed = not(copy.reversed) #its now other players turn
                v = max(v, copy.min_max(new_depth))
        else: #else its player2s turn
            v = 999
            for i in self.find_moves(): #loop through potential moves
                copy = Board(self)
                copy.update_board(i)
                if not(copy.go_again): #if player goes agian we don't update turn flag
                    copy.reversed = not(copy.reversed) #its now other players turn
                v = min(v, copy.min_max(new_depth))
        return v

    #define the alpha beta pruning function to minimize/maximize.
    #the starter code defines it with self, depth=3, alpha=-999, beta=+999.
    #add more parameters if necessary
    #you need to call mim_max here to get the best value
    def alpha_beta(self, depth=3, alpha=-999, beta=+999):
        #initialize values
        v = 0
        best_move = ()
        new_depth = depth - 1
        if not(self.reversed): #if player1s turn do max node computation
            v = -999
            best_move = (0, v)
            #loop through each potetial move
            #for each move create a copy of the board and update the board
            for i in self.find_moves():
                copy = Board(self)
                copy.update_board(i)
                if not(copy.go_again): #if player goes agian we don't update turn flag
                    copy.reversed = not(copy.reversed) #its now other players turn
                v = max(v, copy.min_max(new_depth)) #compare if Heuristic is greater than current value
                alpha = max(alpha, v) 
                if v > best_move[1]:  #if heuristic is better update best move
                    best_move = (i, v)
                if alpha >= beta: # if alpha is >= beta we can prune
                    break
        else: #else its player2s turn and we 
            v = 999
            best_move = (0, v)
            #loop through each potetial move
            #for each move create a copy of the board and update the board
            for i in self.find_moves():
                copy = Board(self)
                copy.update_board(i)
                if not(copy.go_again): #if player goes agian we don't update turn flag
                    copy.reversed = not(copy.reversed) #its now other players turn
                v = min(v, copy.min_max(new_depth)) #compare if Heuristic is less than current value
                beta = min(beta, v)
                if v < best_move[1]: #if heuristic is better update best move
                    best_move = (i, v)
                if alpha >= beta: # if alpha is >= beta we can prune
                    break
        return best_move[0]

    #This function tells you how to caclulate the heuristic score.
    #This should work, changes are not necessary.
    def calculate_heurestic_score(self):
        if not self.reversed:
            return self.player1_points - self.player2_points
        else:
            return self.player2_points - self.player1_points

    #define more helper functions to print current board state here
    def print(self):
        print("         ", end="")
        print(*["%2d" % x for x in reversed(self.board[8:])], sep="|")
        print(
            "P2 --- %2d                  %2d --- P1"
            % (self.player2_points, self.player1_points)
        )
        print("         ", end="")
        print(*["%2d" % x for x in self.board[1:7]], sep="|")
    
#this function defines an object of class Board
#to implement: set the board , according to the starting player (P1 or P2),
#caclulate best moves for players 1 and 2.
#Update the board according to the best move.
#Keep iterating for up to 15 moves total (both players combined) in the future,
#or until the game ends. 
def play_mancala(initial_board=None, starting_player=1):

    board = Board(initial_board)
    if starting_player == 2: #if starting player is P2 set flag
        board.reversed = True
    board.print()
    print()
    #play at least 15 moves or until there is a winner
    for i in range(0, 15):
        #if no moves remaining game is over
        if board.no_moves_remaining():
            print("Game over")
            return
        else:
            move = board.alpha_beta()
            board.update_board(move)
            board.print()
            print()
            #if go_again is true, player moves again
            if board.go_again:
                board.go_again = False
                continue
            else: #else we change reversed flag
                board.reversed = not(board.reversed)
    print("Game Over")

#main is defined here. it takes starting player from the commmand line,
#and calls play_mancala. Initial player is int, either 1 or 2.
#Note: for testing, you can define an initial board here and pass it to
#play_mancala to test different starting conditions.
if __name__ == "__main__":
    player_choice = sys.argv[1]
    print("player choice: ", player_choice)

    default_board = None
    play_mancala(default_board, player_choice)
