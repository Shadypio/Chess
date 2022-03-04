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
            ["--", "--", "--", "--", "bp", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'Q': self.getQueenMoves,
                              'K': self.getKingMoves, 'B': self.getBishopMoves}

        self.whiteToMove = True
        self.moveLog = []

    '''
    Prende una mossa e la esegue 
    (Arrocco, promozione ed en-passant non funzionanti)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Registra la mossa
        self.whiteToMove = not self.whiteToMove

    '''
    Annulla la mossa precedente
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # Deve essere stata fatta una mossa
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    Mosse con scacco (con inchiodatura)
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # Da modificare

    '''
    Mosse senza scacco (senza inchiodatura) 
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Numero di righe
            for c in range(len(self.board[r])): #Numero di colonne della riga r
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # Turno del bianco e muove un pezzo bianco
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # Chiama la funzione appropriata per ogni pezzo
        return moves

    '''
    Genera le mosse del pedone
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # Se la cella avanti è vuota
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # Se la seconda cella avanti è vuota
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 > 0: # Cattura a sinitra
                if self.board[r-1][c-1][0] == 'b': # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 < 7: # Cattura a destra
                if self.board[r-1][c+1][0] == 'b': # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: # Pedone nero
            pass
    '''
    Genera le mosse della torre
    '''
    def getRookMoves(self, r, c, moves):
        pass

    '''
    Genera le mosse del cavallo
    '''
    def getKnightMoves(self, r, c, moves):
        pass

    '''
    Genera le mosse della regina
    '''
    def getQueenMoves(self, r, c, moves):
        pass

    '''
    Genera le mosse della regina
    '''
    def getBishopMoves(self, r, c, moves):
        pass

    '''
    Genera le mosse della regina
    '''
    def getKingMoves(self, r, c, moves):
        pass


class Move():
    # Mappa le chiavi ai valori
    # chiave : valore
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 7,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Override del metodo equals
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

