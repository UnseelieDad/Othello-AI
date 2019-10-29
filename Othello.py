import pygame

pygame.init()

# Constants
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (100, 100, 100)
ORANGE = (255, 140, 0)
RES_X, RES_Y = 1120, 630
ROWS, COLS = 8, 8
BOARD_X, BOARD_Y = 480, 480
SQUARE_X, SQUARE_Y = BOARD_X / 8, BOARD_Y / 8

# Global
isStart = True

# Initialize the the back of the game board and each individual square in an 8x8 grid.
def createBoard():

    # Create a 2d list of board spaces
    # Each board space is a list containing a rectangle and a letter denoting if the space is empty, black, or white
    board = [[[pygame.Rect((0,0),(60,60)), "e"] for j in range(COLS)] for i in range(ROWS)]
    # Create a rectangle to serve as the background for the board
    boardBack = pygame.Rect((0,0),(BOARD_X, BOARD_Y))
    # Set the center of the board to the center of the window
    boardBack.center = ((RES_X / 2), (RES_Y / 2))

    # Find the board's top left corner
    boardCornerX = (RES_X / 2) - (BOARD_X / 2)
    boardCornerY = (RES_Y / 2) - (BOARD_Y / 2)
    offsetX = 0
    offsetY = 0

    # For each space
    for row in board:
        for square in row:
            # Set the square's position based off of the board's top left corner and offset by the size of other squares
            square[0] = square[0].move((boardCornerX + offsetX), (boardCornerY + offsetY))
            offsetX += 60
        
        offsetX = 0
        offsetY += 60

    # If the game is just starting put pieces in the starting positions
    if isStart == True:
        board[3][3][1] = "w"
        board[4][3][1] = "b"
        board[3][4][1] = "b"
        board[4][4][1] = "w"
        isStart == False

    return board, boardBack

# Draw the board on the window
def drawBoard(board, boardBack):
    
    # Draw the board's background
    pygame.draw.rect(screen, GREEN, boardBack)
    
    # Draw the outline for each square
    for row in board:
        for square in row:

            # If the mouse is hovering over the rectangle, change the outline to orange
            if square[0].collidepoint(pygame.mouse.get_pos()):
                rectColor = ORANGE
            else:
                rectColor = BLACK

            pygame.draw.rect(screen, rectColor, square[0], 1)
            # If a square isn't empty draw the appropriate piece there
            if square[1] != "e":
                drawPiece(square)

# Draw a piece of the appropriate color in the center of the given square
def drawPiece(square):

    if square[1] == "b":
        color = BLACK
    elif square[1] == "w":
        color = WHITE

    pygame.draw.circle(screen, color, square[0].center, SQUARE_X / 3)


# Main       

# Create the main window
screen = pygame.display.set_mode((RES_X, RES_Y))
done = False

# Create the board
board, boardBackground = createBoard()

# Main game loop
while not done:
    
    # If the x button on the window is clicked, end the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Wipe the screen        
    screen.fill(BLACK)

    # Draw the board and pieces
    drawBoard(board, boardBackground)

    
    # Update the displaly
    pygame.display.flip()


    # TODO: Othello Rules
    # 50/50 to see who plays white, white goes first
    # Each turn the player places one piece on the board with their color facing up
    # For the first four moves, players must play to one of the four squares in the middle of the board and no pieces are captured or reversed
    # Each Piece must be laid next to an opponents piece such that
    # the opponent's piece or a row of opponent's pieces is flanked by the new piece
    # and another piece of the player's color
    # All oppoent's pieces between these two pieces are captured and turned over to match the player's color
    # It can happen that a piece is played so that pieces or rows of pieces in more than one direction are trapped btween the new piece played
    # and other pieces of the same color. In this case all the pieces in all viable directions are turned over
    # Game ends when neither player can move to capture a piece or the board is full

    # TODO: Features
    # Player 1 and 2 Scores and turn tracking
    # First four turns: Adding a the right color piece when the mouse is clicked, checking for invalid spaces

