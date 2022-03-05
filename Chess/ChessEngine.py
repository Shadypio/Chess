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
            if self.board[r + 1][c] == "--":  # Se la cella avanti è vuota
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # Se la seconda cella avanti è vuota
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Cattura a sinitra
                if self.board[r + 1][c - 1][0] == 'w':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # Cattura a destra
                if self.board[r + 1][c + 1][0] == 'w':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        # Aggiungere promozione pedone

    '''
    Genera le mosse della torre
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Sopra, sinistra, sotto, destra
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Sulla scacchiera
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Spazio vuoto valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Pezzo nemico
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Pezzo amico
                        break
                else: # Fuori scacchiera
                    break

    '''
    Genera le mosse del cavallo
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # L
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Non è un pezzo amico (vuoto o pezzo nemico)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Genera le mosse della regina
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Genera le mosse dell'alfiere
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonali
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Sulla scacchiera
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Spazio vuoto valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Pezzo nemico
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Pezzo amico
                        break
                else:  # Fuori scacchiera
                    break

    '''
    Genera le mosse del re
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))  # Una casella adiacente
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Non è un pezzo amico (vuoto o pezzo nemico)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    # Mappa le chiavi ai valori
    # chiave : valore
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
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

