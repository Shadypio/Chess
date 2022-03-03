"""
Questo file sarà responsabile della gestione degli input dell'utente mostrando il GameState
corrente.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Inizializza un dizionario di immagini. Sarà invocato una sola volta nel main.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Nota: IMAGES['nome_pezzo'] ci consente di accedere al pezzo nome_pezzo

'''
Gestione dell'input dell'utente e aggiornamento della scacchiera. 
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    gameIcon = p.image.load('images/wp.png')
    p.display.set_icon(gameIcon)
    p.display.set_caption("Chess")
    running = True
    sqSelected = () # Tiene traccia del clic dell'utente
    playerClicks = [] # Tiene traccia dei clic dell'utente (due tuple: pezzo selezionato e destinazione)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # Se l'utente ha selezionato due volte la stessa casella
                    sqSelected = () # Deseleziona
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # Dopo il secondo clic
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Gestisce la grafica di un certo GameState.
'''
def drawGameState(screen, gs):
    drawBoard(screen) # Disegna le casella sulla scacchiera
    drawPieces(screen, gs.board) # Disegna i pezzi sulle caselle

'''
Disegna le caselle sulla scacchiera.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''
Disegna i pezzi sulla scacchiera usando il GameState.board corrente
Nota: la casella in alto a sinistra è sempre chiara.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # Non è una cella vuota
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()