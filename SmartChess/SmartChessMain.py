import chess.pgn
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

    #board

if __name__ == "__main__":
    main()