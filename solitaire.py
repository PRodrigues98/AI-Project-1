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

class sol_state:

    def __init__(self, board, num_pegs=0):
        self.board = board
        self.num_pegs = num_pegs

        if num_pegs == 0:
            for row in board:
                for content in row:
                    if is_peg(content):
                        self.num_pegs += 1

    def __lt__(self, state):
        return True

    def get_board(self):
        return self.board

    def get_num_pegs(self):
        return self.num_pegs

class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """

    def __init__(self, board):
        super().__init__(sol_state(board))
        self.board = board

    def actions(self, state):
        board = state.get_board()
        return board_moves(board)

    def result(self, state, action):
        board = state.get_board()
        return sol_state(board_perform_move(board, action), state.get_num_pegs()-1)

    def goal_test(self, state):
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""
        return 0

b1 = [["O","O","O","X","X","X"],
 ["O","_","O","O","O","O"],
 ["O","O","O","O","O","O"],
 ["O","O","O","O","O","O"]]


# print("\nBoard moves: " + str(board_moves(b1)))
# print("\nPerformed move: " + str(board_perform_move(b1,[(0, 2), (0, 0)])))
# print("\nb1: " + str(b1))

sol2 = recursive_best_first_search(solitaire(b1)).solution()
# sol1 = depth_limited_search(solitaire(b1)).solution()

# print(str(sol2) + "\n\n")
print(str(sol1) + "\n\n")

#
# b2 = deepcopy(b1)
#
# for move in sol2:
#     b2 = board_perform_move(b2,move)
#
# print(str(b2) + "\n\n")
#

for move in sol1:
    b1 = board_perform_move(b1,move)

print(str(b1) + "\n\n")


# compare_searchers([solitaire(b1)], 'idk')