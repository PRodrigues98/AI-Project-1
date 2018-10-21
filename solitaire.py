from search import *
from utils import *
from copy import deepcopy
import time

start_time = time.time()


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
def make_pos (l: object, c: object) -> object:
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


def calc_new_average_distance(sum_distance, board, move_beg, move_end):

    move_middle = make_pos((pos_l(move_beg) + pos_l(move_end)) // 2, (pos_c(move_beg) + pos_c(move_end)) // 2)

    for pos in (move_beg, move_middle, move_end):
        for row in range(len(board)):
            for column in range(len(board[row])):
                if is_peg(board[row][column]):
                    if pos_l(pos) == pos_l(move_end) and pos_c(pos) == pos_c(move_end):
                        #average_distance += ((pos_l(pos) - row2) ** 2 + (pos_c(pos) - column2) ** 2) ** 0.5
                        sum_distance += abs(pos_l(pos) - row) + abs(pos_c(pos) - column)
                    else:
                        #average_distance -= ((pos_l(pos) - row2) ** 2 + (pos_c(pos) - column2) ** 2) ** 0.5
                        sum_distance -= abs(pos_l(pos) - row) + abs(pos_c(pos) - column)

    return sum_distance


def calc_sum_distance_from(board, row, column):

    start_column = column + 1
    sum_distance = 0
    for row2 in range(row, len(board)):
        for column2 in range(start_column, len(board[row2])):
            if is_peg(board[row2][column2]):
                #average_distance += ((row - row2) ** 2 + (column - column2) ** 2) ** 0.5
                sum_distance += abs(row - row2) + abs(column - column2) # Lower bound of moves necessary to bring these two pegs together

        start_column = 0
    return sum_distance


def print_board(board):

    for row in board:
        for content in row:
            print(content, end=' ')
        print('')


def is_corner(row, column, board):
    if row == 0 or is_blocked(board[row - 1][column]) or row == len(board) - 1 or is_blocked(board[row + 1][column]):
        if column == 0 or is_blocked(board[row][column - 1]) or column == len(board[0]) - 1 or is_blocked(board[row][column + 1]):
            return True

    return False


class sol_state:
    __slots__ = ('board', 'num_pegs', 'average_distance', 'num_corners')
    def __init__(self, board, num_pegs = 0, average_distance = 0, num_corners = 0):
        self.board = board
        self.num_pegs = num_pegs
        self.average_distance = average_distance
        self.num_corners = num_corners

        if self.num_pegs == 0:
            for row in range(len(board)):
                for column in range(len(board[0])):
                    if is_peg(board[row][column]):
                        self.num_pegs += 1
                        if is_corner(row, column, board):
                            self.num_corners += 1

                        self.average_distance += calc_sum_distance_from(board, row, column)
            self.average_distance /= ((self.num_pegs ** 2 - self.num_pegs) // 2)



    def __lt__(self, state):
        return self.num_pegs > state.get_num_pegs()

    def get_board(self):
        return self.board

    def get_num_pegs(self):
        return self.num_pegs

    def get_average_distance(self):
        return self.average_distance

    def get_num_corners(self):
        return self.num_corners

class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """
    __slots__ = 'board'
    def __init__(self, board):
        super().__init__(sol_state(board))
        self.board = board
        self.i = 0

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        print(self.i)
        self.i += 1
        board = state.get_board()
        new_num_corners = state.get_num_corners() - is_corner(pos_l(move_initial(action)), pos_c(move_initial(action)), board) + is_corner(pos_l(move_final(action)), pos_c(move_final(action)), board)
        new_average_distance = calc_new_average_distance(state.get_average_distance() * ((state.get_num_pegs() ** 2 - state.get_num_pegs()) // 2), state.get_board(), move_initial(action), move_final(action)) / ((state.get_num_pegs() ** 2 - state.get_num_pegs()) // 2)
        print(new_average_distance)
        return sol_state(board_perform_move(board, action), state.get_num_pegs() - 1, new_average_distance, new_num_corners)

    def goal_test(self, state):
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""
        return node.state.get_average_distance() + node.state.get_num_corners() #+ abs(node.state.get_class_difference()) #node.state.get_average_distance() #  #max(node.state.get_num_corners() + node.state.get_num_isolated(), abs(node.state.get_class_difference()))


#def greedy_search(problem, h = None):
#    """f(n) = h(n)"""
#    h = memoize(h or problem.h, 'h')
#    return best_first_graph_search(problem, h)


#b1 = [["O","O","O","X","X"],["O","O","O","O","O"],["O","_","O","_","O"],["O","O","O","O","O"]]
b1 = [['O', 'O', 'O', 'X', 'X', 'X'], ['O', '_', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']]
#sol2 = best_first_graph_search(solitaire(b1), solitaire(b1).h)

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
# astar_search
# greedy_search
sol2 = astar_search(solitaire(b1))

if sol2 != None:
    sol2 = sol2.solution()
    for move in sol2:
        b1 = board_perform_move(b1, move)
    print_board(b1)
    print("\n\n")
else:
    print("No solution")

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

snapshot = tracemalloc.take_snapshot()
display_top(snapshot)

print("--- %s seconds ---" % (time.time() - start_time))                       
