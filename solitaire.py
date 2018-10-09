from search import *
from utils import *
from copy import deepcopy

# TAI content
def c_peg ():
    return "O"

def c_empty ():
    return "_"

def c_blocked ():
    return "X"

def is_empty (e):
    return e == c_empty()

def is_peg (e):
    return e == c_peg()

def is_blocked (e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)

def pos_l (pos):
    return pos[0]

def pos_c (pos):
    return pos[1]

# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]

def move_initial (move):
    return move[0]

def move_final (move):
    return move[1]

def board_moves(board):
    moves = []
    for row in range(len(board)):
        for column in range(len(board[row])):
            if is_peg(board[row][column]):
                if column > 1 and is_peg(board[row][column - 1]) and is_empty(board[row][column - 2]):
                    new_move = make_move(make_pos(row,column), make_pos(row,column - 2))
                    moves.append(new_move)
                if column < len(board[row]) - 2 and is_peg(board[row][column + 1]) and is_empty(board[row][column + 2]):
                    new_move = make_move(make_pos(row,column), make_pos(row,column + 2))
                    moves.append(new_move)
                if row < len(board) - 2 and is_peg(board[row + 1][column]) and is_empty(board[row + 2][column]):
                    new_move = make_move(make_pos(row,column), make_pos(row + 2,column))
                    moves.append(new_move)
                if row > 1 and is_peg(board[row - 1][column]) and is_empty(board[row - 2][column]):
                    new_move = make_move(make_pos(row,column), make_pos(row - 2,column))
                    moves.append(new_move)
    return moves

def board_perform_move(board, move):
    new_board = deepcopy(board)
    move_beg = move_initial(move)
    move_end = move_final(move)

    new_board[pos_l(move_beg)][pos_c(move_beg)] = c_empty()
    new_board[(pos_l(move_beg) + pos_l(move_end)) // 2][(pos_c(move_beg) + pos_c(move_end)) // 2] = c_empty()
    new_board[pos_l(move_end)][pos_c(move_end)] = c_peg()

    return new_board


class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """

    def __init__(self, board):
        Problem.__init__(board)
        self.board = board

    # def actions(self, state):
    #
    # def result(self, state, action):
    # def goal_test(self, state):
    # def path_cost(self, c, state1, action, state2):
    # def h(self, node):
    # 	"""Needed for informed search."""


b1 = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"],
 ["O","_","O","_","_"], ["_","O","_","_","_"]]

print("\nBoard moves: " + str(board_moves(b1)))
print("\nPerformed move: " + str(board_perform_move(b1,[(0, 2), (0, 0)])))
print("\nb1: " + str(b1))