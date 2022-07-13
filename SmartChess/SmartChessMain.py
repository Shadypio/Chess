'''import chess.pgn
import chess.svg
import random
# Visualizzazione partita personale su chess.com

def main():
    myGame()
    print("ciao")

def myGame():
    pgn = open("Matches/newplayernewbielol_vs_Shadypio_2022.03.18.pgn")
    game = chess.pgn.read_game(pgn)

    board = game.board()

    for move in game.mainline_moves():
        board.push(move)

    board

if __name__ == "__main__":
    main()'''


import chess
import chess.engine
import random
import numpy


# this function will create our x (board)
def random_board(max_depth=200):
    board = chess.Board()
    depth = random.randrange(0, max_depth)

    for _ in range(depth):
        all_moves = list(board.legal_moves)
        random_move = random.choice(all_moves)
        board.push(random_move)
        if board.is_game_over():
            break

    return board

# this function will create out f(x) (score)
def stockfish(board, depth):
    with chess.engine.SimpleEngine.popen_uci('C:/Users/Enzuc/Documents/ChessEngine/stockfish_15_x64_avx2.exe') as sf:
        result = sf.analyse(board, chess.engine.Limit(depth=depth))
        score = result['score'].white().score()
        return score

# converts the board representation to something meaningful for the
# neural network
squares_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

# example: h3 -> 17
def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), squares_index[letter[0]]

def split_dims(board):
    # this is the 3d matrix
    board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

    # here we add the pieces's view on the matrix
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    # add attacks and valid moves too
    # so the network knows what is being attacked
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux

    return board3d



board = random_board()
score = stockfish(board, 1)
print(score)
board
(split_dims(board))
