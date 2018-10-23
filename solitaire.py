from search import *
from utils import *
from copy import deepcopy
import time



#start_time = time.time()

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
                    if pos == move_end:
                        if make_pos(row, column) not in (move_beg, move_middle):
                            sum_distance += abs(pos_l(pos) - row) + abs(pos_c(pos) - column)
                    else:
                        sum_distance -= abs(pos_l(pos) - row) + abs(pos_c(pos) - column)
    return sum_distance + 1


def calc_sum_distance_from(board, row, column):

    start_column = column + 1
    sum_distance = 0
    max_distance = 0
    for row2 in range(row, len(board)):
        for column2 in range(start_column, len(board[row2])):
            if is_peg(board[row2][column2]):
                distance = abs(row - row2) + abs(column - column2)
                sum_distance += distance # Lower bound of moves necessary to bring these two pegs together
                if distance > max_distance:
                    max_distance = distance

        start_column = 0

    return sum_distance, max_distance


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

    # old board - 3 checks
    for position in pos_list[:3]:
        if pos_l(position) > 0 and pos_c(position) > 0 and pos_l(position) < len(old_board) and pos_c(position) < len(old_board[0]):
            isolated_diff -= is_peg(old_board[pos_l(position)][pos_c(position)]) and is_isolated(pos_l(position), pos_c(position), old_board) and not is_corner(pos_l(position), pos_c(position), old_board)

    # new board - 5 checks
    for position in pos_list[3:]:
        if pos_l(position) > 0 and pos_c(position) > 0 and pos_l(position) < len(new_board) and pos_c(position) < len(new_board[0]):
            isolated_diff += is_peg(new_board[pos_l(position)][pos_c(position)]) and is_isolated(pos_l(position), pos_c(position), new_board) and not is_corner(pos_l(position), pos_c(position), new_board)

    #print('Action: ', move_beg, move_end)
    #print('Num isolated: ', num_isolated)
    #print('Isolated diff: ', isolated_diff)
    #print_board(old_board)
    #print_board(new_board)
    #if num_isolated + isolated_diff < 0:
    #    sys.exit('oh nono')
    return num_isolated + isolated_diff

class sol_state():
    __slots__ = ('board', 'num_pegs', 'average_distance', 'num_corners', 'num_occupied_corners', 'num_isolated')

    def __init__(self, board, num_pegs = 0, average_distance = 0, num_occupied_corners = 0, num_corners = 0, num_isolated = 0):
        self.board = board
        self.num_pegs = num_pegs
        self.average_distance = average_distance
        self.num_occupied_corners = num_occupied_corners
        self.num_corners = num_corners
        self.num_isolated = num_isolated

        if self.num_pegs == 0:
            for row in range(len(board)):
                for column in range(len(board[0])):
                    if is_peg(board[row][column]):
                        self.num_pegs += 1
                        if is_corner(row, column, board):
                            self.num_occupied_corners += 1
                        if is_isolated(row, column, board):
                            self.num_isolated += 1
                        res = calc_sum_distance_from(board, row, column)
                        self.average_distance += res[0]
                    if not is_blocked(board[row][column]) and is_corner(row, column, board):
                        self.num_corners += 1

            if ((self.num_pegs ** 2 - self.num_pegs) // 2) != 0:
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

    def get_num_isolated(self):
        return self.num_isolated

    def get_num_occupied_corners(self):
        return self.num_occupied_corners

class solitaire(Problem):
    """   Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.   """
    __slots__ = 'board'

    def __init__(self, board):
        super().__init__(sol_state(board))
        self.board = board

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        board = state.get_board()
        new_board = board_perform_move(board, action)

        new_num_occupied_corners = state.get_num_occupied_corners() - is_corner(pos_l(move_initial(action)), pos_c(move_initial(action)), board) + is_corner(pos_l(move_final(action)), pos_c(move_final(action)), board)
        
        if state.get_num_pegs() != 2:
            new_average_distance = calc_new_average_distance(state.get_average_distance() * ((state.get_num_pegs() ** 2 - state.get_num_pegs()) // 2), state.get_board(), move_initial(action), move_final(action)) / (((state.get_num_pegs() - 1) ** 2 - (state.get_num_pegs() - 1)) // 2)
        else:
            new_average_distance = 0
        new_num_isolated = calc_new_isolated(state.get_num_isolated(), board, new_board, move_initial(action), move_final(action))
        return sol_state(new_board, state.get_num_pegs() - 1, new_average_distance, new_num_occupied_corners, state.get_num_corners())

    def goal_test(self, state):
        return state.get_num_pegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        """Needed for informed search."""

        board = node.state.board
        num_pegs_can_move = 0
        n = 0
        for row in range(len(board)):
            for column in range(len(board[0])):
                can_move = False
                if is_peg(board[row][column]):
                    if column > 1 and is_peg(board[row][column - 1]) and is_empty(board[row][column - 2]):
                        can_move = True
                    if column < len(board[row]) - 2 and is_peg(board[row][column + 1]) and is_empty(board[row][column + 2]):
                        can_move = True
                    if row < len(board) - 2 and is_peg(board[row + 1][column]) and is_empty(board[row + 2][column]):
                        can_move = True
                    if row > 1 and is_peg(board[row - 1][column]) and is_empty(board[row - 2][column]):
                        can_move = True
                if can_move:
                    num_pegs_can_move += 1

        h = node.state.get_num_pegs() - num_pegs_can_move

        #print(h)

        if node.state.get_num_pegs() == 1:
            return 0
        else:
            return h

        # distance_weight = 1
        # corner_weight = 1
        # board = node.state.board
        # max_distance = 0

        #for row in range(len(board)):
        #    for column in range(len(board[0])):
        #        if is_peg(board[row][column]):
        #            new_distance = calc_sum_distance_from(board, row, column)[1]
        #            if new_distance > max_distance:
        #                max_distance = new_distance

        # h_distance = node.state.get_average_distance() / max_distance * distance_weight
        # h_corner = (node.state.get_num_occupied_corners() * corner_weight / node.state.get_num_corners())
        # return (node.state.get_num_pegs() - 1) * ((h_distance + h_corner) / (2 + distance_weight + corner_weight))


def greedy_search(problem, h = None):
    """f(n) = h(n)"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)

#b1 = [["O","O","O","X","X"],["O","O","O","O","O"],["O","_","O","_","O"],["O","O","O","O","O"]]
#b1 = [['O', 'O', 'O', 'X', 'X', 'X'], ['O', '_', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']]
#sol2 = best_first_graph_search(solitaire(b1), solitaire(b1).h)

#b1 = [["O","O","O","X","X","X"],
# ["O","_","O","O","O","O"],
# ["O","O","O","O","O","O"],
# ["O","O","O","O","O","O"]]

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

# b1 = [["O","O","O","X"],
# ["O","O","O","O"],
# ["O","_","O","O"],
# ["O","O","O","O"]]

# b1 = [["X","X","O","O","O","O","O","X","X"],
# ["X","X","O","O","O","O","O","X","X"],
# ["O","O","O","O","O","O","O","O","O"],
# ["O","O","O","O","O","O","O","O","O"],
# ["O","O","O","O","_","O","O","O","O"],
# ["O","O","O","O","O","O","O","O","O"],
# ["O","O","O","O","O","O","O","O","O"],
# ["X","X","O","O","O","O","O","X","X"],
# ["X","X","O","O","O","O","O","X","X"]]

# recursive_best_first_search
# astar_search
# greedy_search
#sol2 = astar_search(solitaire(b1))

#if sol2 != None:
#    sol2 = sol2.solution()
#    for move in sol2:
#        b1 = board_perform_move(b1, move)
#        #print_board(b1)
#    print("\n\n")
#else:
#    print("No solution")

#snapshot = tracemalloc.take_snapshot()
#display_top(snapshot)


#print("--- %s seconds ---" % (time.time() - start_time))
