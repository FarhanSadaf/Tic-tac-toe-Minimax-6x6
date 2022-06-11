from cmath import inf
import pygame
from board import Board
pygame.init()

WIDTH = 400-4
HEIGHT = 400-4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()

player = 0
playersigns = {
    0: 'O',     # Human 
    1: 'X'      # AI
}
board = Board(playersigns=playersigns)

def game_over():
    '''
    Checks if there's a winner or all cells of board are filled: True
    Otherwise: False
    '''
    global board, player, playersigns
    winner, cells = Board.check_winner(board.board, playersigns)
    if winner != None:
        print(f'\nPlayer {winner} ({playersigns[winner]}) wins!\n')
        board.draw_line(screen, cells[0], cells[1])
        board.draw_line(screen, cells[1], cells[2])
        board.draw(screen)
        pygame.display.update()
        pygame.time.delay(2000)
        board.clear()
        return True

    if Board.all_filled(board.board):
        print('\nDraw\n')
        board.clear()
        return True
    
    player = (player + 1) % 2
    return False


def minimax(board, depth, alpha, beta, maximizing_player):
    '''
    maximizing player: AI
    '''
    global playersigns
    scores = {
        0: -1,      # Human
        1: +1       #AI
    }
    winner, _ =  Board.check_winner(board, playersigns)
    if winner != None:
        return scores[winner]
    elif Board.all_filled(board) or depth == 0:
        return 0

    if maximizing_player:
        max_eval = -inf
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    board[i][j] = playersigns[1]
                    eval = minimax(board, depth-1, alpha, beta, maximizing_player=False)
                    board[i][j] = ' '
                    max_eval = max(eval, max_eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = inf
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    board[i][j] = playersigns[0]
                    eval = minimax(board, depth-1, alpha, beta, maximizing_player=True)
                    board[i][j] = ' '
                    min_eval = min(eval, min_eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def get_ai_move(board):
    max_score = -inf
    best_move = None
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                board[i][j] = playersigns[1]    # Turn for AI
                score = minimax(board, 3, +inf, -inf, False)    # Turn for Player
                board[i][j] = ' '
                if score > max_score:
                    max_score = score
                    best_move = i, j
    return best_move


while True:
    # Set refresh rate
    clock.tick(60)

    # Event Listener
    for event in pygame.event.get():
        # If cross button event is triggered
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            pos = pygame.mouse.get_pos()
            
            # Human's move
            if board.update(i=pos[1] // (HEIGHT // board.size), j=pos[0] // (HEIGHT // board.size), player=player):
                if game_over():
                    continue
                
                # AI's move
                cell = get_ai_move(board.board)
                board.update(i=cell[0], j=cell[1], player=player)

                if game_over():
                    player = (player + 1) % 2

    # Main drawing stuffs.
    screen.fill((51, 51, 51))
    board.draw(screen)
    pygame.display.update()
