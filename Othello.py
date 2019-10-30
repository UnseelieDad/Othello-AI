'''Othello game program.'''

import pygame
from random import randint

pygame.init()

# Constants
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (100, 100, 100)
ORANGE = (255, 140, 0)
LGREY = (211, 211, 211)
RES_X, RES_Y = 1120, 630
ROWS, COLS = 8, 8
BOARD_X, BOARD_Y = 480, 480
SQUARE_X, SQUARE_Y = BOARD_X / 8, BOARD_Y / 8
CORNER_X, CORNER_Y = (RES_X / 2) - (BOARD_X / 2), (RES_Y / 2) - (BOARD_Y / 2)
FONT = pygame.font.Font("freesansbold.ttf", 32)


# Global
global isStart
global turn
global player1Score
global player2Score
global textList
global player1Color
global player2Color

isStart = True
turn = "b"
player1Score = 0
player2Score = 0
textList = []


# Initialize the the back of the game board and each individual square in an 8x8 grid.
def createBoard():

    # Create a 2d list of board spaces
    # Each board space is a list containing a rectangle and a letter denoting if the space is empty, black, or white
    board = [[[pygame.Rect((0,0),(60,60)), "e"] for j in range(COLS)] for i in range(ROWS)]
    # Create a rectangle to serve as the background for the board
    boardBack = pygame.Rect((0,0),(BOARD_X, BOARD_Y))
    # Set the center of the board to the center of the window
    boardBack.center = ((RES_X / 2), (RES_Y / 2))

    offsetX = 0
    offsetY = 0

    # For each space
    for row in board:
        for square in row:
            # Set the square's position based off of the board's top left corner and offset by the size of other squares
            square[0] = square[0].move((CORNER_X + offsetX), (CORNER_Y + offsetY))
            offsetX += 60       
        offsetX = 0
        offsetY += 60

    # If the game is just starting put pieces in the starting positions
    if isStart is True:
        board[3][3][1] = "w"
        board[4][3][1] = "b"
        board[3][4][1] = "b"
        board[4][4][1] = "w"
        isStart is False

    return board, boardBack

# Draw the board on the window
def drawBoard(board, boardBack):

    # Draw the board's background
    pygame.draw.rect(screen, GREEN, boardBack)
    
    # Draw the outline for each square
    for row in board:
        for square in row:
            # If the mouse is hovering over the rectangle, change the outline to orange
            if square[1] is "h":
                rectColor = ORANGE
            else:
                rectColor = BLACK

            pygame.draw.rect(screen, rectColor, square[0], 1)
 
            # If a square isn't empty draw the appropriate piece there
            if square[1] is "b" or square[1] is "w":
                drawPiece(square)

# Draw a piece of the appropriate color in the center of the given square
def drawPiece(square):

    if square[1] == "b":
        color = BLACK
    elif square[1] == "w":
        color = WHITE

    pygame.draw.circle(screen, color, square[0].center, SQUARE_X / 3)

def createText():

    player1Text = FONT.render("Player 1 Score:", True, GREEN)
    player1TextRect = player1Text.get_rect()
    player1TextRect.center = ((CORNER_X / 2),(CORNER_Y / 2))

    player2Text = FONT.render("Player 2 Score:", True, GREEN)
    player2TextRect = player2Text.get_rect()
    player2TextRect.center = ((BOARD_X + CORNER_X * 1.5), (CORNER_Y / 2))

    if first is 1:
        turnText = FONT.render("Player 1's Turn", True, GREEN)
    else:
        turnText = FONT.render("Player 2's Turn", True, GREEN)
    turnTextRect = turnText.get_rect()
    turnTextRect.center = ((RES_X / 2), (BOARD_Y + CORNER_Y * 1.5))

    player1ScoreText = FONT.render("{}".format(player1Score), True, GREEN)
    player1ScoreTextRect = player1ScoreText.get_rect()
    player1ScoreTextRect.center = (player1TextRect.center[0], (player1TextRect.center[1] + 40))

    player2ScoreText = FONT.render("{}".format(player2Score), True, GREEN)
    player2ScoreTextRect = player2ScoreText.get_rect()
    player2ScoreTextRect.center = (player2TextRect.center[0], (player2TextRect.center[1] + 40))

    textList.extend([(player1Text, player1TextRect), (player2Text, player2TextRect), (turnText, turnTextRect), (player1ScoreText, player1ScoreTextRect), (player2ScoreText, player2ScoreTextRect)])

def updateTurn():

    global turn
    
    if turn is "b":
        turn = "w"
    else:
        turn = "b"

    if textList[2]:
        oldTurnText = textList.pop(2)

        if turn is player1Color:
            newTurnText = (FONT.render("Player 1's Turn", True, GREEN), oldTurnText[1])
        else:
            newTurnText = (FONT.render("Player 2's Turn", True, GREEN), oldTurnText[1])

        textList.insert(2, newTurnText)   

def updateScore():

    #global textList    
    global textList

    player1ScoreTextRect = textList[3][1]
    player2ScoreTextRect = textList[4][1]

    # If there are scores in the list remove them.
    if len(textList) > 3:
        textList = textList[:-2]

    player1ScoreText = FONT.render("{}".format(player1Score), True, GREEN)
    player2ScoreText = FONT.render("{}".format(player2Score), True, GREEN)



    textList.extend([(player1ScoreText, player1ScoreTextRect), (player2ScoreText, player2ScoreTextRect)])

def drawText():

    for text in textList:
        screen.blit(text[0], text[1])

def getValidSpaces(board):

    validSpaces = []
    # integers representing directions
    # Starts with 1 = left and counts up and clockwise through 8 directions
    # 1: left 2: up and left 3: up 4: up and right 5: right 6: down and right 7: down 8: down and left
    enemyDirections = []

    flankedPieces = []

    validMoves = []

    for x in range(ROWS):
        for y in range(COLS):
            currentSpace = board[x][y]
            if turn is "b":
                oppositeColor = "w"
            else:
                oppositeColor = "b"
            
            # check space to the left
            if x > 1:
                if board[x - 1][y][1] is oppositeColor:
                    for z in range(2,x):
                        if board[x - z][y][1] is turn:
                            enemyDirections.append(1)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # Check spaces to the right
            if x < 7:
                if board[x + 1][y][1] is oppositeColor:
                    for z in range(2, COLS - x):
                        if board[x + z][y][1] is turn:
                            enemyDirections.append(5)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break
            
            # check spaces above
            if y > 1:
                if board[x][y - 1][1] is oppositeColor:
                    for z in range(2,y):
                        if board[x][y-z][1] is turn:
                            enemyDirections.append(3)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # check spaces below
            if y < 7:
                if board[x][y + 1][1] is oppositeColor:
                    for z in range(2, ROWS - y):
                        if board[x][y + z][1] is turn:
                            enemyDirections.append(7)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # check up and left
            if x > 1 and y > 1:
                if board[x - 1][y - 1][1] is oppositeColor:
                    for zx, zy in zip(range(2,x), range(2,y)):
                        if board[x - z][y - z][1] is turn:
                            enemyDirections.append(2)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # check down and right
            if x < 7 and y < 7:
                if board[x + 1][y + 1][1] is oppositeColor:
                    for zx, zy in zip(range(2, COLS - x), range(ROWS - y)):
                        if board[x + zx][y + zy][1] is turn:
                            enemyDirections.append(6)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # check down and left
            if x > 1 and y < 7:
                if board[x - 1][y + 1][1] is oppositeColor:
                    for zx, zy in zip(range(2, x), range(2, ROWS - y)):
                        if board[x - z][y + z][1] is turn:
                            enemyDirections.append(7)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break

            # check up and right
            if x < 7 and y > 1:
                if board[x + 1][y - 1][1] is oppositeColor:
                    for zx, zy in zip(range(2, COLS - x), range(2,y)):
                        if board[x + z][y - z][1] is turn:
                            enemyDirections.append(4)
                            if currentSpace not in validSpaces:
                                validSpaces.append(currentSpace)
                            break
            flankedPieces.append(tuple(enemyDirections))
            enemyDirections = []

    validMoves = zip(validSpaces, flankedPieces)

    return validMoves

def flipLines(space, validMoves, board):

    print validMoves

    for move in validMoves:
        if space is move[0]:
            print move
            flipDirections = move[1]
            print flipDirections
            break

    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y] is space:
                for direction in flipDirections:
                    if direction is 1:
                        for z in range(1,x):
                            if board[x-z][y][1] is turn:
                                break
                            else:
                                # flip the piece
                                flipPiece(board[x-z][y])
                        continue
                    if direction is 2:
                        for zx, zy in zip(range(1,x), range(1,y)):
                            if board[x-zx][y-zy][1] is turn:
                                break
                            else:
                                flipPiece(board[x-zx][y-zy])
                        continue
                    if direction is 3:
                        for z in range(1,y):
                            if board[x][y-z][1] is turn:
                                break
                            else:
                                flipPiece(board[x][y-z])
                        continue
                    if direction is 4:
                        for zx, zy in zip(range(1, COLS-x), range(1,y)):
                            if board[x+zx][y-zy][1] is turn:
                                break
                            else:
                                flipPiece(board[x+zx][y-zy])
                        continue
                    if direction is 5:
                        for z in range(1, COLS-x):
                            if board[x+z][y][1] is turn:
                                break
                            else:
                                flipPiece(board[x+z][y])
                        continue
                    if direction is 6:
                        for zx, zy in zip(range(1, COLS-x), range(1,ROWS-y)):
                            if board[x+zx][y+zy][1] is turn:
                                break
                            else:
                                flipPiece(board[x+zx][y+zy])
                        continue
                    if direction is 7:
                        for z in range(1, ROWS-y):
                            if board[x][y+z][1] is turn:
                                break
                            else:
                                flipPiece(board[x][y+z])
                        continue
                    if direction is 8:
                        for zx, zy in zip(range(1,x), range(1,ROWS-y)):
                            if board[x-zx][y+zy][1] is turn:
                                break
                            else:
                                flipPiece(board[x-zx][y+zy])
                break



def flipPiece(square):

    if turn is "b":
        square[1] = "w"
    else:
        square[1] = "b"


    

# Main       

# See who's going first
first = randint(1,2)
if first is 1:
    player1Color = "b"
    player2Color = "w"
else:
    player2Color = "b"
    player1Color = "w"

# Create the main window
screen = pygame.display.set_mode((RES_X, RES_Y))
pygame.display.set_caption("Othello")


# Create the board
board, boardBackground = createBoard()

# Create text
createText()

# Main game loop
done = False
while not done:
    
    # calculate valid spaces based off of the current board state
    validMoves = getValidSpaces(board)

    # Main events loop
    # If the x button on the window is clicked, end the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # If the mouse moves or is clicked
        if event.type is pygame.MOUSEMOTION or event.type is pygame.MOUSEBUTTONUP:
            # Get the mouse's position
            pos = pygame.mouse.get_pos()
            
            # For each square on the board
            for row in board:
                for square in row:
                    # If the mouse is over the square and the square is empty
                    if square[0].collidepoint(pos) and square[1] is not "b" and square[1] is not "w":
                        # if it was a click place a piece
                        if event.type is pygame.MOUSEBUTTONUP and square[1] is "h":
                            if turn is "b": 
                                square[1] = "b"
                            else:
                                square[1] = "w"
                            flipLines(square, validMoves, board)

                            updateTurn()
                        # If the mouse moved, and if the space is valid, highlight the square
                        if event.type is pygame.MOUSEMOTION:
                            for move in validMoves:
                                if square is move[0]:
                                    square[1] = "h"
                    # Un-highlight any square the mouse doesn't touch or isn't valid
                    elif square[1] is "h":
                        square[1] = "e"

    # Wipe the screen
    screen.fill(BLACK)

    # Draw the board and pieces
    drawBoard(board, boardBackground)

    # Draw text elements on the screen
    drawText()
    
    # Update the displaly
    pygame.display.flip()


    # TODO:
    # Valid space: Space where you'll be able to flip at least one opposing disk after placement: check
    # Forfeit key/message for when there aren't any valid moves
    # Placed disk can flip all directions if valid. Hor, vert, diag
    # Only flips opposing pieces between disks
    # Can only flip disks in a direct line from the placed disk
    # Scoring

