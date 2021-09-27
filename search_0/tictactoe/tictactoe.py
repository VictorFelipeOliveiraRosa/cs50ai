"""
Tic Tac Toe Player
"""
import copy
import math
from random import choice

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def count_piece(board):
    count_x = 0
    count_o = 0

    for row in board:
        for column in row:
            if column == X:
                count_x += 1
            if column == O:
                count_o += 1

    return count_x, count_o


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x, count_o = count_piece(board=board)

    if count_x == 0 or count_o == count_x:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = list()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                possible_moves.append((row, column))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_moves = actions(board)
    play = player(board)
    new_board = copy.deepcopy(board)
    for move in possible_moves:
        if action == move:
            new_board[action[0]][action[1]] = play
            return new_board

    raise ValueError("JOGADA INVÁLIDA")


# p_c == player_current


def check_board(board, p_c):
    # horizontal
    if board[0][0] == p_c and board[0][1] == p_c and board[0][2] == p_c:
        return True
    if board[1][0] == p_c and board[1][1] == p_c and board[1][2] == p_c:
        return True
    if board[2][0] == p_c and board[2][1] == p_c and board[2][2] == p_c:
        return True

    # vertical
    if board[0][0] == p_c and board[1][0] == p_c and board[2][0] == p_c:
        return True
    if board[0][1] == p_c and board[1][1] == p_c and board[2][1] == p_c:
        return True
    if board[0][2] == p_c and board[1][2] == p_c and board[2][2] == p_c:
        return True

    # diagonal
    if board[0][0] == p_c and board[1][1] == p_c and board[2][2] == p_c:
        return True
    if board[0][2] == p_c and board[1][1] == p_c and board[2][0] == p_c:
        return True

    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_board(board, X):
        return X
    if check_board(board, O):
        return O

    return None


def tied_game(board):
    for row in board:
        for column in row:
            if column == EMPTY:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    if tied_game(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    play_winner = winner(board)
    if play_winner == X:
        return 1
    elif play_winner == O:
        return -1
    else:
        return 0


def node(
    state, board, children=[], heuristica=0, n_moves=0, node_terminal=False
):
    return {
        "move": state,
        "board": board,
        "children": children,
        "heuristica": heuristica,
        "n_moves": n_moves,
        "node_terminal": node_terminal,
    }


def play_one(board):
    piece_x, piece_o = count_piece(board)

    moves_possible = [
        (0, 0),
        (0, 2),
        (2, 0),
        (2, 2),
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1),
    ]
    # moves_possible_1 = [(0, 1), (1, 0), (1, 2), (2, 1)]
    if piece_x == 0 and piece_o == 0:
        return choice(moves_possible)
    elif piece_x == 1 and piece_o == 0:
        for move in moves_possible:
            if board[move[0]][move[1]] == X:
                return (1, 1)
        # for move in moves_possible_1:
        #     if board[move[0]][move[1]] == X:
        #         return (1, 1)

    return None


def who_winner(score, play_who):
    if play_who == X and score == 1:
        return True
    if play_who == O and score == -1:
        return True
    return False


def verify_play_opponent(board, move, play_OPPONENT):
    copy_board = []
    copy_board = copy.deepcopy(board)
    copy_board[move[0]][move[1]] = play_OPPONENT
    # if terminal(copy_board):
    #     value_move = utility(copy_board)
    #     if who_winner(value_move, play_OPPONENT):
    #         return True
    if check_board(copy_board, play_OPPONENT):
        return True
    return False


def population_tree(board_current, n_moves, play_Ai):
    lista = []
    possible_moves = actions(board_current)
    play_Human = X
    if play_Ai == X:
        play_Human = O

    for move in possible_moves:
        new_board = result(board_current, move)
        new_node = node(move, new_board, [], None, n_moves + 1, False)

        if verify_play_opponent(new_board, move, play_Ai):
            new_node["heuristica"] = 1 + n_moves + 1
            new_node["node_terminal"] = True

        elif verify_play_opponent(new_board, move, play_Human):
            new_node["heuristica"] = -1 + (-n_moves + 1)
            new_node["node_terminal"] = True
        elif tied_game(new_board):
            new_node["heuristica"] = 0
            new_node["node_terminal"] = True

        lista.append(new_node)
    return lista


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # tree = list()
    play_AI = player(board)
    move_now = play_one(board)
    if move_now:
        return move_now

    tree_test = list()
    board_current = copy.deepcopy(board)
    tree_test = population_tree(board_current, 0, play_AI)

    def pop_in(node):
        if not node["node_terminal"]:
            if len(node["children"]) == 0:
                new_node = population_tree(
                    node["board"],
                    node["n_moves"],
                    play_AI,
                )
                if len(new_node) > 0:
                    node["children"] = list(new_node)
            if len(node["children"]) > 0:
                for x_node in node["children"]:
                    pop_in(x_node)

    # node_main = node((), board, [], 0, 0, False)
    for x_node in tree_test:
        pop_in(x_node)
    # node_main["children"] = copy.deepcopy(tree_test)

    def ai_minimax(node, profundidade):
        if node["node_terminal"] or profundidade <= 0:
            return node["heuristica"], node["n_moves"]
        else:
            score = 0
            n_moves = 0
            bestscore = -math.inf
            for x_node in node["children"]:
                score, n_moves = ai_minimax(x_node, profundidade - 1)
                score = max(-score, bestscore)

            return score, n_moves
        # else:
        #     bestscore = math.inf
        #     for x_node in node["children"]:
        #         score, n_moves = ai_minimax(x_node, profundidade - 1, False)
        #         print("MAXIMIZADOR  PROFUNDIDADE:  ", profundidade)
        #         print("SCORE ->  ", score, " MOVE -->  ", n_moves, "\n")
        #         score = min(bestscore, score)
        #     return score, n_moves

    for x_node in tree_test:
        if not x_node["node_terminal"]:
            score, n_moves = ai_minimax(x_node, 10000)
            x_node["heuristica"] = score
            x_node["n_moves"] = n_moves

    # tree_test = ai_minimax(node_main, 100000, False)

    tree_test.sort(
        key=lambda x: (
            x["node_terminal"],
            -x["n_moves"],
            x["heuristica"],
        ),
        reverse=True,
    )

    if tree_test[0]["node_terminal"]:
        return tree_test[0]["move"]

    tree_test.sort(
        key=lambda x: (
            x["heuristica"],
            -x["n_moves"],
        ),
        reverse=True,
    )

    # # tree_test.sort(key=lambda x: x["n_moves"])

    return tree_test[0]["move"]
