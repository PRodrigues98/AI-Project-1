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


def calc_atributes(board):
    num_pegs = 0
    num_occupied_corners = 0
    num_isolated = 0
    first_peg_slot = None
    average_distance = 0

    for row in range(len(board)):
        for column in range(len(board[0])):
            if is_peg(board[row][column]):
                num_pegs += 1
                if is_corner(row, column, board):
                    num_occupied_corners += 1
                if is_isolated(row, column, board):
                    num_isolated += 1
                if not first_peg_slot:
                    average_distance = calc_sum_distance_from(board, row, column)
                    first_peg_slot = make_pos(row, column)

    if num_pegs != 0:
        average_distance /= num_pegs

    return num_pegs, num_occupied_corners, num_isolated, first_peg_slot, average_distance

def find_new_first_peg(board):

    for row in range(len(board)):
        for column in range(len(board[0])):
            if is_peg(board[row][column]):
                return make_pos(row, column)


class sol_state():
    __slots__ = ('board', 'num_pegs', 'average_distance', 'num_occupied_corners', 'num_isolated', 'first_peg_slot')

    def __init__(self, board, num_pegs = 0, average_distance = 0, num_occupied_corners = 0, num_isolated = 0, first_peg_slot = None):
        self.board = board
        self.num_pegs = num_pegs
        self.num_occupied_corners = num_occupied_corners
        self.num_isolated = num_isolated
        self.first_peg_slot = first_peg_slot
        self.average_distance = average_distance

        if self.num_pegs == 0:
            self.num_pegs, self.num_occupied_corners, self.num_isolated, self.first_peg_slot, self.average_distance = calc_atributes(self.board)

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
    __slots__ = ('board')

    def __init__(self, board):
        super().__init__(sol_state(board))
        self.board = board

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        board = state.get_board()
        new_board = board_perform_move(board, action)

        new_num_occupied_corners = state.get_num_occupied_corners() - is_corner(pos_l(move_initial(action)), pos_c(move_initial(action)), board) + is_corner(pos_l(move_final(action)), pos_c(move_final(action)), board)
        new_num_isolated = calc_new_isolated(state.get_num_isolated(), board, new_board, move_initial(action), move_final(action))

        if move_initial(action) == state.get_first_peg_slot() or move_final(action) == state.get_first_peg_slot():
            new_first_peg_slot = find_new_first_peg(new_board)
            new_average_distance = calc_sum_distance_from(new_board, pos_l(new_first_peg_slot), pos_c(new_first_peg_slot)) / (state.get_num_pegs() - 1)
        else:
            new_average_distance = (state.get_average_distance() * state.get_num_pegs() + calc_diff_distance(state.get_first_peg_slot(), move_initial(action), move_final(action))) / (state.get_num_pegs() - 1)
            new_first_peg_slot = state.get_first_peg_slot()

        return sol_state(new_board, state.get_num_pegs() - 1, new_average_distance, new_num_occupied_corners, new_num_isolated, new_first_peg_slot)

    def goal_test(self, state):
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""

        h = node.state.get_average_distance() * len(node.state.board) + node.state.get_num_occupied_corners() * len(node.state.board) * len(node.state.board[0]) + node.state.get_num_isolated() * len(node.state.board) * len(node.state.board[0])

        if node.state.get_num_pegs() == 1:
            return 0
        else:
            return h