"""
Questa classe conserva le informazioni sullo stato corrente della partita.
Inoltre, verifica quali sono le mosse valide nello stato corrente e tiene traccia
delle mosse compiute.
"""


class GameState():
    def __init__(self):
        # La scacchiera è una lista 2d 8x8, ogni elemento della lista ha 2 caratteri.
        # Il primo carattere rappresenta il colore, il secondo la sigla del pezzo.
        # "--" rappresenta una casella vuota.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
