'''Othello game program.'''

import pygame
from Node import Node
from random import randint
from time import sleep
from copy import deepcopy

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
global compActive
global compPlayer

isStart = True
turn = "b"
player1Score = 0
player2Score = 0
textList = []
compActive = True
compPlayer = 2

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

def setBottomText(text):

    if textList[2]:
        oldTurnText = textList.pop(2)

    newTurnText = (FONT.render(text, True, GREEN), oldTurnText[1])

    textList.insert(2, newTurnText)

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

    player1Score = 0
    player2Score = 0

    for row in gameBoard:
        for square in row:
            if square[1] is player1Color:
                player1Score += 1
            elif square[1] is player2Color:
                player2Score += 1

    player1ScoreTextRect = textList[3][1]
    player2ScoreTextRect = textList[4][1]

    # If there are scores in the list remove them.
    if len(textList) > 3:
        textList = textList[:-2]

    player1ScoreText = FONT.render("{}".format(player1Score), True, GREEN)
    player2ScoreText = FONT.render("{}".format(player2Score), True, GREEN)



    textList.extend([(player1ScoreText, player1ScoreTextRect), (player2ScoreText, player2ScoreTextRect)])

def drawText(screen):

    for text in textList:
        screen.blit(text[0], text[1])

def getValidSpaces(board):

    validSpaces = []
    # integers representing directions
    # Starts with 1 = left and counts up and clockwise through 8 directions
    # 1: left 2: up and left 3: up 4: up and right 5: right 6: down and right 7: down 8: down and left

    flankedPieces = 0
    flankDirections = []

    for x in range(ROWS):
        for y in range(COLS):
            currentSpace = board[x][y]
            if turn is "b":
                oppositeColor = "w"
            else:
                oppositeColor = "b"
            
            # check space to the left
            if y > 1:
                if board[x][y-1][1] is oppositeColor:
                    for z in range(2,x):
                        if board[x][y-z][1] is turn:
                            #print "left"
                            flankDirections.append(1)
                            break

            # Check spaces to the right
            if y < 7:
                if board[x][y + 1][1] is oppositeColor:
                    for z in range(2, COLS - y):
                        if board[x][y+z][1] is turn:
                            #print "right"
                            flankDirections.append(5)
                            break
            
            # check spaces above
            if x > 1:
                if board[x-1][y][1] is oppositeColor:
                    for z in range(2,y):
                        if board[x-z][y][1] is turn:
                            #print "up"
                            flankDirections.append(3)
                            break

            # check spaces below
            if x < 7:
                if board[x+1][y][1] is oppositeColor:
                    for z in range(2, ROWS - x):
                        if board[x+z][y][1] is turn:
                            #print "down"
                            flankDirections.append(7)
                            break

            # check up and left
            if x > 1 and y > 1:
                if board[x - 1][y - 1][1] is oppositeColor:
                    for zx, zy in zip(range(2,x), range(2,y)):
                        if board[x - zx][y - zy][1] is turn:
                            flankDirections.append(2)
                            break

            # check down and right
            if x < 7 and y < 7:
                if board[x + 1][y + 1][1] is oppositeColor:
                    for zx, zy in zip(range(2, ROWS - x), range(2, COLS - y)):
                        if board[x + zx][y + zy][1] is turn:
                            flankDirections.append(6)
                            break

            # check down and left
            if x < 7 and y > 1:
                if board[x+1][y-1][1] is oppositeColor:
                    for zx, zy in zip(range(2, ROWS - x), range(2, y)):
                        if board[x+zx][y-zy][1] is turn:
                            flankDirections.append(8)
                            break

            # check up and right
            if x > 1 and y < 7:
                if board[x - 1][y + 1][1] is oppositeColor:
                    for zx, zy in zip(range(2, x), range(2, COLS - y)):
                        if board[x - zx][y + zy][1] is turn:
                            flankDirections.append(4)
                            break
            
            if len(flankDirections) is not 0:
                validSpaces.append((currentSpace, flankDirections))
            flankDirections = []

    return validSpaces

def flipLines(square, validMoves, board):
    
    x = 0
    y = 0

    for move in validMoves:
        if square is move[0]:
            directions = move[1]
            

    for row, rows in enumerate(board):
        if square in rows:
            x = row
            y = rows.index(square)


    if square is board[x][y]:
        for direction in directions:
            zx = x
            zy = y

            if direction is 1:
                while True:
                    zy -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 2:
                while True:
                    zy -= 1
                    zx -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 3:
                while True:
                    zx -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 4:
                while True:
                    zx -= 1
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 5:
                while True:
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 6:
                while True:
                    zx += 1
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 7:
                while True:
                    zx += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            elif direction is 8:
                while True:
                    zx += 1
                    zy -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])

def flipPiece(square):

    if square[1] is not "e" and square[1] is not "h":
        if square[1] is "b":
            square[1] = "w"
        else:
            square[1] = "b"
    
def printBoard(board):

    printRow = []

    for row in board:
        for space in row:
            if space[1] is "e":
                printRow.append(' ')
            else:
                printRow.append(space[1])
        print(printRow)
        printRow = []


class Othello_AI:

    # Requirements:
    # Easily adjustable search depth
    # Computer can play white or black
    # Debug mode that prints out sequences of moves considered from current state with associated heuristic value
    # Debug can be toggled on a move by move basis
    # Debug mode that indicates when a branch is pruned and which branch is pruned
    # Implements mini-max
    # Implements alpha-beta pruning

    def __init__(self, levelsDeep, board):
        self.levelsDeep = levelsDeep
        self.currentBoard = board

    def generateChildren(self, node, maxLevel, currentLevel):

        global turn
        startingNodeTurn = turn
        spaceFound = False
        sourceBoard = node.data
        initialState = deepcopy(sourceBoard)
       
       # Get valid moves from the board state stored in the current node
        validMoves = getValidSpaces(sourceBoard)

        # Create a child node for the board state that results from each valid move
        for space in validMoves:
            # create a new board starting as the current node's board state

            for row in sourceBoard:
                if spaceFound is True:
                    break

                for square in row:
                    # if the square on the new board matches a valid move
                    if space[0][0] is square[0]:
                        # place a piece of the appropriate color and flip the flanked pieces to create a new board state
                        square[1] = turn

                        flipLines(square, validMoves, sourceBoard)
                        spaceFound = True
                        break

            # Create a node with the new board state and add it to the current node's children
            newBoard = deepcopy(sourceBoard)
            childState = Node(newBoard)
            node.addChild(childState)

            # Reset source board
            for x in range(ROWS):
                for y in range(COLS):
                    sourceBoard[x][y][1] = initialState[x][y][1]

            spaceFound = False

        currentLevel += 1

        if currentLevel is not maxLevel:

            if turn is "b":
                turn = "w"
            else:
                turn = "b"

            for child in node.children:
                self.generateChildren(child, self.levelsDeep, currentLevel)
        
        elif currentLevel is maxLevel:
            childHeuristics = []
            for child in node.children:
                # run heuristic function on theb board state
                #set child's heuristic
                pass

        for child in node.children:
            if currentLevel % 2 is 0:
                # maximizing level
                # set this node's heuristic to the highest
                pass
            else:
                # minimizing level
                # set this node's heuristic to the lowest
                pass

        turn = startingNodeTurn

    def generateTree(self):
    
        
        # source is the first node
        source = Node(self.currentBoard)

        # starting a level 0 of the tree
        level = 0

        self.generateChildren(source, self.levelsDeep, level)

        return source

    def setCurrentBoardState(self, newBoardState):
        self.currentBoard = newBoardState

    def runHeuristics(self, node):
        # Calculate coin parity
        # Calculate Mobility
        # Calculate number of corners captured
        # Calculate stability

        pass

    def coinParityHeuristic(self, board):
        p1Score = 0
        p2Score = 0

        for row in board:
            for space in row:
                if space[1] is player1Color:
                    p1Score += 1
                elif space[1] is player2Color:
                    p2Score += 1
        
        # Check if the level the heuristic is being run on is a minimizing level or a maximizing level
        if self.levelsDeep % 2 is 0:
            maxPlayerScore = p2Score
            minPlayerScore = p1Score
        else:
            maxPlayerScore = p1Score
            minPlayerScore = p2Score
        
        heuristic = 100 * (maxPlayerScore - minPlayerScore) / (maxPlayerScore + minPlayerScore)

        return heuristic
        
    def mobilityHeuristic(self, board):
        
        global turn
        originalTurn = turn

        turn = player2Color
        moves = getValidSpaces(board)
        player2Mobility = len(moves)

        turn = player1Color
        moves = getValidSpaces(board)
        player1Mobility = len(moves)

        # Check if the level the heuristic is being run on is a minimizing level or a maximizing level
        if self.levelsDeep % 2 is 0:
            maxPlayerMobility = player2Mobility
            minPlayerMobility = player1Mobility
        else:
            maxPlayerMobility = player1Mobility
            minPlayerMobility = player2Mobility

        if player2Mobility + player1Mobility is not 0:
            heuristic = 100 * (maxPlayerMobility - minPlayerMobility) / (maxPlayerMobility + minPlayerMobility)
        else:
            heuristic = 0
        
        return heuristic

    def cornerHeuristic(self, board):
        
        player1Corners = 0
        player2Corners = 0
        
        if board[0][0][1] is player1Color:
            player1Corners += 1
        elif board[0][0][1] is player2Color:
            player2Color += 1

        if board[0][8][1] is player1Color:
            player1Corners += 1
        elif board[0][8][1] is player2Color:
            player2Color += 1

        if board[8][0][1] is player1Color:
            player1Corners += 1
        elif board[8][0][1] is player2Color:
            player2Color += 1

        if board[8][8][1] is player1Color:
            player1Corners += 1
        elif board[8][8][1] is player2Color:
            player2Color += 1

        # Check if the level the heuristic is being run on is a minimizing level or a maximizing level
        if self.levelsDeep % 2 is 0:
            maxPlayerCorner = player2Corners
            minPlayerCorner = player1Corners
        else:
            maxPlayerCorner = player1Corners
            minPlayerCorner = player2Corners
        
        if player2Corners + player1Corners is not 0:
            heuristic = 100 * (maxPlayerCorner - minPlayerCorner) / (maxPlayerCorner + minPlayerCorner)
        else:
            heuristic = 0

        return heuristic

    def stabliityHeuristic(self, board):
        
        stableSpaces = []
        unstableSpaces = []

        player1Stability = 0
        player2Stability = 0
        
        for x in range(ROWS):
            for y in range(COLS):

                if board[x][y][1] is not "e" and board[x][y][1] is not "h":
                    if checkStable(board, stableSpaces, x, y):
                        stableSpaces.append(board[x][y])
                        break
                    elif checkUnstable(board, x, y):
                        unstableSpaces.append(board[x][y])
        
        for space in stableSpaces:
            if space[1] is player1Color:
                player1Stability += 1
            elif space[1] is player2Color:
                player2Stability += 1

        for space in unstableSpaces:
            if space[1] is player1Color:
                player1Stability -= 1
            elif space[1] is player2Color:
                player2Stability -= 1

        # Check if the level the heuristic is being run on is a minimizing level or a maximizing level
        if self.levelsDeep % 2 is 0:
            maxPlayerStability = player2Stability
            minPlayerStability = player1Stability
        else:
            maxPlayerStability = player1Stability
            minPlayerStability = player2Stability

        if player2Stability + player1Stability is not 0:
            heuristic = 100 * (maxPlayerStability - minPlayerStability) / (maxPlayerStability + minPlayerStability)
        else:
            heuristic = 0

        return heuristic
                    
    def checkUnstable(self, board, x, y):
        # If piece can be taken in the next move it is unstable
        global turn
        originalTurn = turn
        if board[x][y][1] is "b":
            turn = "w"
        else:
            turn = "b"

        moves = getValidSpaces(board)

        adjacentSpaces = [board[x+1][y], board[x-1][y], board[x][y+1], board[x][y-1], board[x-1][y-1], board[x+1][y+1], board[x-1][y+1], board[x+1][y-1]]

        for space in moves:
            if space[0][0] in adjacentSpaces:
                turn = originalTurn
                return True

        turn = originalTurn
        return False
    
    def checkStable(self, board, stableSpaces, x, y):

        # check left and right
        stableHor = True
        # Piece is stable horizontally if the row is full
        for zy in range(0,y):
            if board[x][zy][1] is "e":
                stableHor = False
        if stableHor is not False:
            for zy in range(y,8):
                if board[x][zy][1] is "e":
                    stableHor = False
        # if row isn't full, piece is stable horizontally if it's next to an edge or another stable piece
        if stableHor is False:
            if y is 0 or y is 7:
                stableHor = True
            elif board[x][y - 1] in stableSpaces or board[x][y + 1] in stableSpaces:
                stableHor = True
        
        # check vertically
        stableVert = True
        for zx in range(0,x):
            if board[zx][y][1] is "e":
                stableVert = False
        if stableVert is not False:
            for zx in range(x,8):
                if board[zx][y][1] is "e":
                    stableVert = False
        # if column isn't full, piece is stable vertically if it's next to an edge or another stable piece
        if stableVert is False:
            if x is 0 or x is 7:
                stableVert = True
            elif board[x - 1][y] in stableSpaces or board[x + 1][y] in stableSpaces:
                stableVert = True
        
        # check diagonals
        stableDiagBack = True
        for zx, zy in zip(range(0,x), range(0,y)):
            if board[zx][zy][1] is "e":
                stableDiagBack = False
        if stableDiagBack is False:
            for zx, zy in zip(range(x,8), range(y,8)):
                if board[zx][zy][1] is "e":
                    stableDiagBack = False
        if stableDiagBack is False:
            if x is 0 and y is 0 or x is 7 and y is 7:
                stableDiagBack = True
            elif board[x - 1][y - 1] in stableSpaces or board[x + 1][y + 1] in stableSpaces:
                stableDiagBack = True
        
        stableDiagFront = True
        for zx, zy in zip(range(0,x), range(y,8)):
            if board[zx][zy][1] is "e":
                stableDiagFront = False
        if stableDiagFront is False:
            for zx, zy in zip(range(x,8), range(0,y)):
                if board[zx][zy][1] is "e":
                    stableDiagFront = False
        if stableDiagFront is False:
            if x is 0 and y is 0 or x is 7 and y is 7:
                stableDiagFront = True
            elif board[x + 1][y - 1] in stableSpaces or board[x + 1][y - 1] in stableSpaces:
                stableDiagFront = True

        if stableHor and stableVert and stableDiagBack and stableDiagFront:
            return True
        else:
            return False

    def printTree(self, node):

        printBoard(node.data)
        print

        if node.children:
            for child in node.children:
                self.printTree(child)



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
gameBoard, boardBackground = createBoard()

# Create text
createText()

if compActive is True:
    comp = Othello_AI(3, deepcopy(gameBoard))

noValidMovesCounter = 0

# Main game loop
done = False
while not done:
    
    # calculate valid spaces based off of the current board state
    validMoves = getValidSpaces(gameBoard)

    

    # Main events loop
    # If the x button on the window is clicked, end the game
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            done = True

        # if there are no valid moves on a player's turn the player must forefiet the turn
        if len(validMoves) is 0:
            noValidMovesCounter += 1
            if noValidMovesCounter is 2:
                # Game over function, need to grab final scores and throw it up at the end
                if player1Score > player2Score:
                    winText = "Player 1 Wins!"
                else:
                    winText = "Player 2 Wins!"
                bottomText = "Game Over: "
                setBottomText(bottomText+winText)
            else:
                bottomText = "No valid moves. Press the F key to forefiet the turn."
                setBottomText(bottomText)
                while True:
                    if event.type is pygame.KEYDOWN:
                        if event.key is pygame.K_f:
                            updateTurn()
                            break
                    elif event.type is pygame.QUIT:
                        done = True
                        break
        elif noValidMovesCounter > 0:
            noValidMovesCounter = 0

        # If the mouse moves or is clicked
        if compActive is False or compActive is True and turn is player1Color:
            if event.type is pygame.MOUSEMOTION or event.type is pygame.MOUSEBUTTONUP:
                # Get the mouse's position
                pos = pygame.mouse.get_pos()
                
                # For each square on the board
                for row in gameBoard:
                    for square in row:
                        # If the mouse is over the square and the square is empty
                        if square[0].collidepoint(pos) and square[1] is not "b" and square[1] is not "w":
                            # if it was a click place a piece
                            if event.type is pygame.MOUSEBUTTONUP and square[1] is "h":
                                
                                print validMoves

                                flipLines(square, validMoves, gameBoard)
                                
                                square[1] = turn
                                
                                updateTurn()
                            # If the mouse moved, and if the space is valid, highlight the square
                            if event.type is pygame.MOUSEMOTION:
                                for move in validMoves:
                                    if square is move[0]:
                                        square[1] = "h"
                        # Un-highlight any square the mouse doesn't touch or isn't valid
                        elif square[1] is "h":
                            square[1] = "e"
        
        elif compActive is True and turn is player2Color:
            # AI turn
            # Generate new tree
            print "AI taking turn."
            sleep(3)
            print "Generating tree"
            decisionTree = comp.generateTree()
            print "Tree Generated"
            # Run algorithms
            # Make the best move
            updateTurn()

    comp.setCurrentBoardState(gameBoard)

    # Update the score
    updateScore()

    # Wipe the screen
    screen.fill(BLACK)

    # Draw the board and pieces
    drawBoard(gameBoard, boardBackground)

    # Draw text elements on the screen
    drawText(screen)
    
    # Update the displaly
    pygame.display.flip()


    # TODO:
    # 
    # game over/win message
    # Scoring

