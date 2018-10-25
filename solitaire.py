from search import *
from utils import *
from copy import deepcopy
import time

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


def move_initial(move):
    return move[0]


def move_final(move):
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


def calc_diff_distance(pivot, move_beg, move_end):
    move_middle = make_pos((pos_l(move_beg) + pos_l(move_end)) // 2, (pos_c(move_beg) + pos_c(move_end)) // 2)

    return abs(pos_l(move_end) - pos_l(pivot)) + abs(pos_c(move_end) - pos_c(pivot)) - (abs(pos_l(move_beg) - pos_l(pivot)) + abs(pos_c(move_beg) - pos_c(pivot))) - (abs(pos_l(move_middle) - pos_l(pivot)) + abs(pos_c(move_middle) - pos_c(pivot)))


def calc_sum_distance_from(board, row, column):

    sum_distance = 0

    for row2 in range(len(board)):
        for column2 in range(len(board[row2])):
            if is_peg(board[row2][column2]):
                sum_distance += abs(row - row2) + abs(column - column2) # Lower bound of moves necessary to bring these two pegs together
    return sum_distance


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


def calc_new_isolated(num_isolated, old_board, new_board, move_beg, move_end):

    isolated_diff = 0
    middle_row = (pos_l(move_beg) + pos_l(move_end)) // 2
    middle_column = (pos_c(move_beg) + pos_c(move_end)) // 2

    move_direction_row = pos_l(move_beg) - middle_row
    move_direction_column = middle_column - pos_c(move_beg)

    # positions to check
    #     5  3  2
    #  7  P  P  me 0
    #     6  4  1
    pos0 = make_pos(pos_l(move_end) + move_direction_row, pos_c(move_end) + move_direction_column)
    pos1 = make_pos(pos_l(move_end) - move_direction_column, pos_c(move_end) - move_direction_row)
    pos2 = make_pos(pos_l(move_end) + move_direction_column, pos_c(move_end) + move_direction_row)
    pos3 = make_pos(middle_row - move_direction_column, middle_column - move_direction_row)
    pos4 = make_pos(middle_row + move_direction_column, middle_column + move_direction_row)
    pos5 = make_pos(pos_l(move_beg) - move_direction_column, pos_c(move_beg) - move_direction_row)
    pos6 = make_pos(pos_l(move_beg) + move_direction_column, pos_c(move_beg) + move_direction_row)
    pos7 = make_pos(pos_l(move_beg) - move_direction_row, pos_c(move_beg) - move_direction_column)

    pos_list = (pos0, pos1, pos2, pos3, pos4, pos5, pos6, pos7, move_end)

    # old board : 3 checks
    for position in pos_list[:3]:
        if 0 < pos_l(position) < len(old_board) and 0 < pos_c(position) < len(old_board[0]):
            isolated_diff -= is_peg(old_board[pos_l(position)][pos_c(position)]) and is_isolated(pos_l(position), pos_c(position), old_board) and not is_corner(pos_l(position), pos_c(position), old_board)

    # new board : 5 checks
    for position in pos_list[3:]:
        if 0 < pos_l(position) < len(new_board) and 0 < pos_c(position) < len(new_board[0]):
            isolated_diff += is_peg(new_board[pos_l(position)][pos_c(position)]) and is_isolated(pos_l(position), pos_c(position), new_board) and not is_corner(pos_l(position), pos_c(position), new_board)

    return num_isolated + isolated_diff


class sol_state():
    __slots__ = ('board', 'num_pegs', 'average_distance', 'num_occupied_corners', 'num_isolated', 'first_peg_slot')

    def __init__(self, board, num_pegs = 0, average_distance = 0, num_occupied_corners = 0, num_isolated = 0, first_peg_slot = None):
        self.board = board
        self.num_pegs = num_pegs
        self.average_distance = average_distance
        self.num_occupied_corners = num_occupied_corners
        self.num_isolated = num_isolated
        self.first_peg_slot = first_peg_slot

        if self.num_pegs == 0:
            for row in range(len(board)):
                for column in range(len(board[0])):
                    if is_peg(board[row][column]):
                        self.num_pegs += 1
                        if is_corner(row, column, board):
                            self.num_occupied_corners += 1
                        if is_isolated(row, column, board):
                            self.num_isolated += 1
                        if not self.first_peg_slot:
                            self.average_distance = calc_sum_distance_from(board, row, column)
                            self.first_peg_slot = make_pos(row, column)
            if self.num_pegs != 0:
                self.average_distance /= self.num_pegs

    def __lt__(self, state):
        return self.num_pegs > state.get_num_pegs()

    def get_board(self):
        return self.board

    def get_num_pegs(self):
        return self.num_pegs

    def get_average_distance(self):
        return self.average_distance

    def get_num_isolated(self):
        return self.num_isolated

    def get_num_occupied_corners(self):
        return self.num_occupied_corners

    def get_first_peg_slot(self):
        return self.first_peg_slot


class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """
    __slots__ = ('board', 'num_nos_gerados', 'num_nos_expandidos')

    def __init__(self, board):
        super().__init__(sol_state(board))
        self.board = board
        self.num_nos_expandidos = 0
        self.num_nos_gerados = 0

    def actions(self, state):
        moves = board_moves(state.get_board())
        return moves

    def result(self, state, action):
        self.num_nos_expandidos += 1
        board = state.get_board()
        new_board = board_perform_move(board, action)

        new_num_occupied_corners = state.get_num_occupied_corners() - is_corner(pos_l(move_initial(action)), pos_c(move_initial(action)), board) + is_corner(pos_l(move_final(action)), pos_c(move_final(action)), board)
        new_num_isolated = calc_new_isolated(state.get_num_isolated(), board, new_board, move_initial(action), move_final(action))

        if move_initial(action) == state.get_first_peg_slot() or move_final(action) == state.get_first_peg_slot():
            for row in range(len(new_board)):
                for column in range(len(new_board[0])):
                    if is_peg(new_board[row][column]):
                        new_first_peg_slot = make_pos(row, column)
                        new_average_distance = calc_sum_distance_from(new_board, row, column) / (
                                    state.get_num_pegs() - 1)
                        return sol_state(new_board, state.get_num_pegs() - 1, new_average_distance,
                                         new_num_occupied_corners, new_num_isolated,
                                         new_first_peg_slot)
        else:
            new_average_distance = (state.get_average_distance() * state.get_num_pegs() + calc_diff_distance(state.get_first_peg_slot(), move_initial(action), move_final(action))) / (state.get_num_pegs() - 1)
            return sol_state(new_board, state.get_num_pegs() - 1, new_average_distance, new_num_occupied_corners, new_num_isolated, state.get_first_peg_slot())

    def goal_test(self, state):
        self.num_nos_gerados += 1
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""

        h = node.state.get_average_distance() * len(node.state.board) + (node.state.get_num_occupied_corners() + node.state.get_num_isolated()) * len(node.state.board) * len(node.state.board[0])

        if node.state.get_num_pegs() == 1:
            return 0
        else:
            return h


def greedy_search(problem, h = None):
    """f(n) = h(n)"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)

#b1 = entrega31 = [["O","O","O","X","X"],["O","O","O","O","O"],["O","_","O","_","O"],["O","O","O","O","O"]]
#b1 = entrega32 = [['O', 'O', 'O', 'X', 'X', 'X'], ['O', '_', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']]

test1 = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"], ["O","_","O","_","_"], ["_","O","_","_","_"]]

test2 = [["O","O","O","X"], ["O","O","O","O"], ["O","_","O","O"], ["O","O","O","O"]]

test3 = [["O","O","O","X","X"], ["O","O","O","O","O"], ["O","_","O","_","O"], ["O","O","O","O","O"]]

test4 = [["O","O","O","X","X","X"], ["O","_","O","O","O","O"], ["O","O","O","O","O","O"], ["O","O","O","O","O","O"]]

for searcher in (greedy_search, astar_search, depth_first_tree_search):
    print(str(searcher))
    num = 0
    for test in (test1, test2, test3, test4):
        start_time = time.time()
        sol1 = solitaire(test)
        sol2 = searcher(sol1)
        print("Test" + str(num + 1) + " --- %s seconds --- " % (time.time() - start_time) + " --- %s Nos Gerados --- " % sol1.num_nos_gerados + " --- %s Nos Expandidos --- " % sol1.num_nos_expandidos)
        num += 1

#tests:
# depth_first_tree_search
# greedy_search
# astar_search

#snapshot = tracemalloc.take_snapshot()
#display_top(snapshot)

#compare_searchers([solitaire(test1), solitaire(test2), solitaire(test3), solitaire(test4)],
#                  ['Searcher', 'Test1', 'Test2', 'Test3', 'Test4'],
#                  [greedy_search, astar_search])