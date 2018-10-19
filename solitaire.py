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
                    new_move = make_move(make_pos(row, column), make_pos(row, column - 2))
                    moves.append(new_move)
                if column < len(board[row]) - 2 and is_peg(board[row][column + 1]) and is_empty(board[row][column + 2]):
                    new_move = make_move(make_pos(row, column), make_pos(row, column + 2))
                    moves.append(new_move)
                if row < len(board) - 2 and is_peg(board[row + 1][column]) and is_empty(board[row + 2][column]):
                    new_move = make_move(make_pos(row, column), make_pos(row + 2, column))
                    moves.append(new_move)
                if row > 1 and is_peg(board[row - 1][column]) and is_empty(board[row - 2][column]):
                    new_move = make_move(make_pos(row, column), make_pos(row - 2, column))
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

def is_corner(row, column, board):

    if row == 0 or is_blocked(board[row - 1][column]) or row == len(board) - 1 or is_blocked(board[row + 1][column]):
        if column == 0 or is_blocked(board[row][column - 1]) or column == len(board[0]) - 1 or is_blocked(board[row][column + 1]):
            return True

    return False

def is_isolated(row, column, board):

    if (row >= 0 and column == 0) or (column > 0 and is_empty(board[row][column - 1])):
        if column == len(board[row]) - 1 or (column < len(board[row]) - 1 and is_empty(board[row][column + 1])):
            if row == len(board) - 1 or (row < len(board) - 1 and is_empty(board[row + 1][column])):
                if row == 0 or (row > 0 and is_empty(board[row - 1][column])):
                    return not is_corner(row, column, board)

    return False



class sol_state:
    def __init__(self, board, num_pegs = 0, num_corners = 0, num_same_parity = 0): # num_isolated = 0
        __slot__ = 'board', 'num_pegs', 'num_corners', 'num_isolated', 'num_same_parity'
        self.board = board
        self.num_pegs = num_pegs
        self.num_corners = num_corners
        #self.num_isolated = num_isolated
        self.num_same_parity = num_same_parity

        if num_pegs == 0:
            for row in range(len(board)):
                for column in range(len(board[row])):
                    if is_peg(board[row][column]):
                        self.num_pegs += 1
                        if is_corner(row, column, board):
                            self.num_corners += 1
                        #if is_isolated(row, column, board):
                        #    self.num_isolated += 1
                        if column % 2 == row % 2:
                            self.num_same_parity += 1

    def __lt__(self, state):
        return self.num_pegs > state.get_num_pegs()

    def get_board(self):
        return self.board

    def get_num_pegs(self):
        return self.num_pegs

    def get_num_corners(self):
        return self.num_corners

    #def get_num_isolated(self):
    #    return self.num_isolated

    def get_num_same_parity(self):
        return self.num_same_parity

    def get_class_difference(self):
        return self.num_same_parity - (self.num_pegs - self.num_same_parity)


class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """

    def __init__(self, board):
        super().__init__(sol_state(board))
        __slot__ = 'board'
        self.board = board

    def actions(self, state):
        board = state.get_board()

        if abs(state.get_class_difference()) == state.get_num_pegs():
            #print("Crisis averted " + str(state.get_class_difference()) + " " + str(state.get_num_pegs()))
            return []

        return board_moves(board)

    def result(self, state, action):
        board = state.get_board()

        new_num_pegs = state.get_num_pegs() - 1


        start = move_initial(action)
        end = move_final(action)

        new_num_corners = state.get_num_corners() - is_corner(pos_l(start), pos_c(start), board) + is_corner(pos_l(end), pos_c(end), board)
        new_num_same_parity = state.get_num_same_parity() - (pos_l(start) % 2 != pos_c(start) % 2)
        #print(str(new_num_pegs) + " " + str(state.get_num_same_parity()) + " " + str(pos_l(start)) + " " + str(pos_c(start)))
        #new_num_isolated = state.get_num_isolated() - is_isolated(pos_l(start) - 1, pos_c(start), board) - is_isolated(pos_l(start), pos_c(start), board) - is_isolated(pos_l(start), pos_c(start), board) - is_isolated(pos_l(start), pos_c(start), board) + is_isolated(pos_l(start), pos_c(start), board)

        return sol_state(board_perform_move(board, action), new_num_pegs, new_num_corners, new_num_same_parity)

    def goal_test(self, state):
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""

        return node.state.get_num_corners() #node.state.get_num_isolated()


#b1 = [["O","O","O","X","X","X"],
#["O","_","O","O","O","O"],
#["O","O","O","O","O","O"],
#["O","O","O","O","O","O"]]

#b1 = [['X','_','_','_','X'],
#['_','_','_','_','O'],
#['O','O','_','O','_'],
#['_','_','_','_','_'],
#['X','_','_','_','X']]

#b1 = [['X','O','O','O','X'],
#['O','O','O','O','O'],
#['O','O','_','O','O'],
#['O','O','O','O','O'],
#['X','O','O','O','X']]

#b1 = [["O","O","O","X"],
#["O","O","O","O"],
#["O","_","O","O"],
#["O","O","O","O"]]

#b1 = [["X","X","O","O","O","O","O","X","X"],
#["X","X","O","O","O","O","O","X","X"],
#["O","O","O","O","O","O","O","O","O"],
#["O","O","O","O","O","O","O","O","O"],
#["O","O","O","O","_","O","O","O","O"],
#["O","O","O","O","O","O","O","O","O"],
#["O","O","O","O","O","O","O","O","O"],
#["X","X","O","O","O","O","O","X","X"],
#["X","X","O","O","O","O","O","X","X"]]

# print("\nBoard moves: " + str(board_moves(b1)))
# print("\nPerformed move: " + str(board_perform_move(b1,[(0, 2), (0, 0)])))
# print("\nb1: " + str(b1))


# recursive_best_first_search
#sol2 = astar_search(solitaire(b1))

#if sol2 != None:
#    sol2 = sol2.solution()

#    for move in sol2:
#        b1 = board_perform_move(b1, move)

#    print(str(b1) + "\n\n")
#else:
#    print("No solution")
#sol2 = recursive_best_first_search(solitaire(b1)).solution()
# sol1 = depth_limited_search(solitaire(b1)).solution()

#print(str(sol2) + "\n\n")
# print(str(sol1) + "\n\n")


#same_parity = 0
#isolated = 0
#corners = 0

#for row in range(len(b1)):
#    for column in range(len(b1[row])):
#        if is_peg(b1[row][column]):
#            if is_corner(row, column, b1):
#                corners += 1
#            if is_isolated(row, column, b1):
#                isolated += 1
#            if column % 2 == row % 2:
#                same_parity += 1

#print(str(isolated) + " " + str(corners) + " " + str(same_parity))

#
# b2 = deepcopy(b1)
#

#
# print(str(b2) + "\n\n")
#

# for move in sol1:
#     b1 = board_perform_move(b1,move)


# compare_searchers([solitaire(b1)], 'idk')
