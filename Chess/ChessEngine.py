"""
Questa classe conserva le informazioni sullo stato corrente della partita.
Inoltre, verifica quali sono le mosse valide nello stato corrente e tiene traccia
delle mosse compiute.
"""

import pygame as p

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
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()  # Coordinate della cella disponibile per en passant
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]


    '''
    Esamina una mossa e la esegue 
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Registra la mossa
        self.whiteToMove = not self.whiteToMove
        # Aggiorna la posizione del re, se necessario
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Promozione pedone a Regina
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # EnPassant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # Solo se il pedone avanza di due case
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()

        # Arrocco
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Arrocco corto
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]  # Muove la torre nella nuova casella
                self.board[move.endRow][move.endCol+1] = '--'  # Toglie la torre dalla vecchia posizione
            else:  # Arrocco lungo
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]  # Muove la torre nella nuova casella
                self.board[move.endRow][move.endCol-2] = '--'

        # Aggiorna diritto ad arrocco - se re o torre vengono mossi
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    '''
    Annulla la mossa precedente
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # Deve essere stata fatta una mossa
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # Aggiorna la posizione del re, se necessario
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # Annulla en passant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            # Annulla un avanzamento di 2 case di un pedone
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

            # Annulla diritto ad arrocco
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # Annulla arrocco
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # Arrocco corto
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:  # Arrocco lungo
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkMate = False
            self.staleMate = False



    '''
    Aggiorna il diritto ad arrocco della mossa move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # Torre sinistra
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # Torre destra
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # Torre sinistra
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # Torre destra
                    self.currentCastlingRight.bks = False


    '''
    Mosse con scacco (con inchiodatura)
    '''
    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # 1.) Generare tutte le mosse
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # 2.) Per ogni mossa, fai la mossa
        for i in range(len(moves)-1, -1, -1):  # Quando rimuovi dalla lista, naviga all'indietro
            self.makeMove(moves[i])

            # 3.) Genera tutte le mosse dell'avversario
            # 4.) Per ogni mossa avversario, verifica se attacca il re
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                # 5.) Se attacca il re, non è una mossa valida
                moves.remove(moves[i])

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:  # Scaccomatto o stallo
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    '''
    Verifica se il giocatore è sotto scacco
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Verifica se il nemico attacca la casa r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # Cambia il turno
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Cambia il turno
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # La casa è sotto attacco
                return True
        return False


    '''
    Mosse senza scacco (senza inchiodatura) 
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # Numero di righe
            for c in range(len(self.board[r])):  # Numero di colonne della riga r
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):  # Turno del bianco e muove un pezzo bianco
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # Chiama la funzione appropriata per ogni pezzo
        return moves

    '''
    Genera le mosse del pedone
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":  # Se la cella avanti è vuota
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # Se la seconda cella avanti è vuota
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 > 0:  # Cattura a sinistra
                if self.board[r-1][c-1][0] == 'b':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnPassantMove=True))
            if c+1 < 7:  # Cattura a destra
                if self.board[r-1][c+1][0] == 'b':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r - 1, c + 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnPassantMove=True))

        else:  # Pedone nero
            if self.board[r + 1][c] == "--":  # Se la cella avanti è vuota
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # Se la seconda cella avanti è vuota
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Cattura a sinistra
                if self.board[r + 1][c - 1][0] == 'w':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 <= 7:  # Cattura a destra
                if self.board[r + 1][c + 1][0] == 'w':  # Pezzo nemico da catturare
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnPassantMove=True))
        # Aggiungere promozione pedone

    '''
    Genera le mosse della torre
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Sopra, sinistra, sotto, destra
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

    '''
    Genera le mosse per arroccare
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # Impossibile arroccare sotto scacco
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3 == '--']:
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    # Mappa le chiavi ai valori
    # chiave : valore
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Promozione
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)

        # En passant
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        # Arrocco
        self.isCastleMove = isCastleMove

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
