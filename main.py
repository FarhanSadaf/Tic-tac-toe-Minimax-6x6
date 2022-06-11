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

playerscores = {
    0: 0,
    1: 0
}

board = Board(playersigns=playersigns)
checked_winners = [[False for _ in range(board.size)] for _ in range(board.size)]

def game_over():
    '''
    Checks if there's a winner or all cells of board are filled: True
    Otherwise: False
    '''
    global player, playerscores
    if Board.all_filled(board.board):
        print('\nFinal score :')
        print(f'Player {playerscores[0]}')
        print(f'AI {playerscores[1]}', end='\n\n')

        if playerscores[0] == playerscores[1]:
            print('\nDraw!')
        elif playerscores[0] > playerscores[1]:
            print('\nPlayer won!')
        else:
            print('\nAI won!')

        pygame.time.delay(2000)
        board.clear()
        board.draw_board(screen)
        pygame.display.update()
        
        player = 0
        playerscores = {
            0: 0,
            1: 0
        }
        return True

    return False


def check_winner():
    global board, winner_checked, playersigns, playerscores
    line_color = {
        0: (255, 255, 255),
        1: (255, 99, 71)
    }
    winner, cells = Board.check_winner(board.board, checked_winners, playersigns)
    if winner != None:
        playerscores[winner] += 1

        print(f'Player {playerscores[0]}')
        print(f'AI {playerscores[1]}', end='\n\n')
        
        board.draw_line(screen, cells[0], cells[1], line_color[winner])
        board.draw_line(screen, cells[1], cells[2], line_color[winner])
        
        for i, j in cells:
            checked_winners[i][j] = True
            
        pygame.display.update()

def minimax(board, depth, alpha, beta, maximizing_player):
    '''
    maximizing player: AI
    '''
    global playersigns, checked_winners
    scores = {
        0: -1,      # Human
        1: +1       #AI
    }
    winner, _ =  Board.check_winner(board, checked_winners, playersigns)
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

# Draw initaial board
board.draw_board(screen)
pygame.display.update()

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
            
            # Player's move
            if board.update(i=pos[1] // (WIDTH // board.size), j=pos[0] // (HEIGHT // board.size), player=player):
                check_winner()

                board.draw_moves(screen)
                pygame.display.update()
                
                if game_over():
                    continue
                
                # AI's move
                player = (player + 1) % 2
                cell = get_ai_move(board.board)

                board.update(i=cell[0], j=cell[1], player=player)
                check_winner()

                board.draw_moves(screen)
                pygame.display.update()
                
                # Player's move
                player = (player + 1) % 2
                game_over()
