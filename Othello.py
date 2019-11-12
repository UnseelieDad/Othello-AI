# Seth Martin
# CWID: 10252074
# 11/11/19
# Assignment 3
# This program implements the board game Othello in graphical form.
# This proram facilitates play by two human players or one human and
# an AI player.

# THe Graphical library used
import pygame
# Node class for generating tree
from Node import Node
# For randomly deciding who's black
from random import randint
# To slow the AI down a little
from time import sleep
# To make copies of the board states
from copy import deepcopy

# Initialize pygame
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
global gameOver
global p1NoMove
global p2NoMove
global foundGameOver
global turnCount
global DEBUG


isStart = True
turn = "b"
player1Score = 0
player2Score = 0
player1Color = ""
player2Color = ""
textList = []
compActive = True
p1NoMove = False
p2NoMove = False
gameOver = False
foundGameOver = False
turnCount = 1
DEBUG = False

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

# Create inital text displayed on the screen
def createText():

    # Create player 1 text
    player1Text = FONT.render("Player 1 Score:", True, GREEN)
    player1TextRect = player1Text.get_rect()
    player1TextRect.center = ((CORNER_X / 2),(CORNER_Y / 2))

    # Create player 2 text
    player2Text = FONT.render("Player 2 Score:", True, GREEN)
    player2TextRect = player2Text.get_rect()
    player2TextRect.center = ((BOARD_X + CORNER_X * 1.5), (CORNER_Y / 2))

    # If player 1 is first set bottom text to player 1's turn
    # Otherwise, set it to player 2
    if first is 1:
        turnText = FONT.render("Player 1's Turn", True, GREEN)
   
    else:
        turnText = FONT.render("Player 2's Turn", True, GREEN)
    
    turnTextRect = turnText.get_rect()
    turnTextRect.center = ((RES_X / 2), (BOARD_Y + CORNER_Y * 1.5))

    # Create player 1's score
    player1ScoreText = FONT.render("{}".format(player1Score), True, GREEN)
    player1ScoreTextRect = player1ScoreText.get_rect()
    player1ScoreTextRect.center = (player1TextRect.center[0], (player1TextRect.center[1] + 40))

    # Create player 2's score
    player2ScoreText = FONT.render("{}".format(player2Score), True, GREEN)
    player2ScoreTextRect = player2ScoreText.get_rect()
    player2ScoreTextRect.center = (player2TextRect.center[0], (player2TextRect.center[1] + 40))

    # Add text to text list
    textList.extend([(player1Text, player1TextRect), (player2Text, player2TextRect), (turnText, turnTextRect), (player1ScoreText, player1ScoreTextRect), (player2ScoreText, player2ScoreTextRect)])

# Set the text at the bottom of the window to a passed-in string
def setBottomText(text, screen):

    # If bottom text exists in list, remove old text
    if textList[2]:
        oldTurnText = textList.pop(2)

    # Create new text using the old text's rectangle
    newTurnText = (FONT.render(text, True, GREEN), oldTurnText[1])

    # Add text back to the list, draw it to the screen, and update the screen.
    textList.insert(2, newTurnText)
    drawText(screen)
    pygame.display.flip()

# Update whose turn it is
def updateTurn():

    global turn
    global turnCount

    turnCount += 1
    print "Turn: {}\n".format(turnCount)
    
    # Switch turns
    if turn is "b":
        turn = "w"
    else:
        turn = "b"

    # Update turn text at the bottom of the screen
    if textList[2]:
        oldTurnText = textList.pop(2)

        if turn is player1Color:
            newTurnText = (FONT.render("Player 1's Turn", True, GREEN), oldTurnText[1])
        else:
            newTurnText = (FONT.render("Player 2's Turn", True, GREEN), oldTurnText[1])

        textList.insert(2, newTurnText)   

# Update player scores
def updateScore():

    #global textList    
    global textList

    player1Score = 0
    player2Score = 0

    # count discs for each player and add them up
    for row in gameBoard:
        for square in row:
            if square[1] is player1Color:
                player1Score += 1
            elif square[1] is player2Color:
                player2Score += 1

    print "Player 1 Score: {}".format(player1Score)
    print "Player 2 Score: {}".format(player2Score)
    print

    # Get old display rectangles
    player1ScoreTextRect = textList[3][1]
    player2ScoreTextRect = textList[4][1]

    # If there are scores in the list remove them.
    if len(textList) > 3:
        textList = textList[:-2]

    # Make new score text based on new scores
    player1ScoreText = FONT.render("{}".format(player1Score), True, GREEN)
    player2ScoreText = FONT.render("{}".format(player2Score), True, GREEN)

    # Add new scores back to the list
    textList.extend([(player1ScoreText, player1ScoreTextRect), (player2ScoreText, player2ScoreTextRect)])

# Draw all text to the screen
def drawText(screen):

    for text in textList:
        screen.blit(text[0], text[1])

# From the current board state, all valid moves for the current player
def getValidSpaces(board):

    validSpaces = []
    # integers representing directions
    # Starts with 1 = left and counts up and clockwise through 8 directions
    # 1: left 2: up and left 3: up 4: up and right 5: right 6: down and right 7: down 8: down and left

    flankedPieces = 0
    flankDirections = []

    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y][1] is "e" or board[x][y] is "h":
                currentSpace = board[x][y]
                if turn is "b":
                    oppositeColor = "w"
                else:
                    oppositeColor = "b"
                
                # check space to the left
                if y > 1:
                    if board[x][y-1][1] is oppositeColor:
                        for z in range(2,y):
                            if board[x][y-z][1] is not "b" and board[x][y-z][1] is not "w":
                                break
                            elif board[x][y-z][1] is turn:
                                #print "left"
                                flankDirections.append(1)
                                break

                # Check spaces to the right
                if y < 7:
                    if board[x][y + 1][1] is oppositeColor:
                        for z in range(2, COLS - y):
                            if board[x][y+z][1] is not "b" and board[x][y+z][1] is not "w":
                                break
                            elif board[x][y+z][1] is turn:
                                #print "right"
                                flankDirections.append(5)
                                break
                
                # check spaces above
                if x > 1:
                    if board[x-1][y][1] is oppositeColor:
                        for z in range(2,x):
                            if board[x-z][y][1] is not "b" and board[x-z][y][1] is not "w":
                                break
                            elif board[x-z][y][1] is turn:
                                #print "up"
                                flankDirections.append(3)
                                break

                # check spaces below
                if x < 7:
                    if board[x+1][y][1] is oppositeColor:
                        for z in range(2, ROWS - x):
                            if board[x+z][y][1] is not "b" and board[x+z][y][1] is not "w":
                                break
                            elif board[x+z][y][1] is turn:
                                #print "down"
                                flankDirections.append(7)
                                break

                # check up and left
                if x > 1 and y > 1:
                    if board[x - 1][y - 1][1] is oppositeColor:
                        for zx, zy in zip(range(2,x), range(2,y)):
                            if board[x - zx][y - zy][1] is not "b" and board[x - zx][y - zy][1] is not "w":
                                break
                            elif board[x - zx][y - zy][1] is turn:
                                flankDirections.append(2)
                                break

                # check down and right
                if x < 7 and y < 7:
                    if board[x + 1][y + 1][1] is oppositeColor:
                        for zx, zy in zip(range(2, ROWS - x), range(2, COLS - y)):
                            if board[x + zx][y + zy][1] is not "b" and board[x + zx][y + zy][1] is not "w":
                                break
                            elif board[x + zx][y + zy][1] is turn:
                                flankDirections.append(6)
                                break

                # check down and left
                if x < 7 and y > 1:
                    if board[x+1][y-1][1] is oppositeColor:
                        for zx, zy in zip(range(2, ROWS - x), range(2, y)):
                            if board[x+zx][y-zy][1] is not "b" and board[x+zx][y-zy][1] is not "w":
                                break
                            elif board[x+zx][y-zy][1] is turn:
                                flankDirections.append(8)
                                break

                # check up and right
                if x > 1 and y < 7:
                    if board[x - 1][y + 1][1] is oppositeColor:
                        for zx, zy in zip(range(2, x), range(2, COLS - y)):
                            if board[x - zx][y + zy][1] is not "b" and board[x - zx][y + zy][1] is not "w":
                                break
                            if board[x - zx][y + zy][1] is turn:
                                flankDirections.append(4)
                                break
                
                if len(flankDirections) is not 0:
                    validSpaces.append((currentSpace, flankDirections))
                flankDirections = []

    # Return a list of the valid moves and directions of flanked pieces from that space
    return validSpaces

# Once a piece is placed, flip all the flanked pieces
def flipLines(square, validMoves, board):
    
    x = 0
    y = 0

    directions = []

    # Get the flanking directions for the square the piece was placed in
    for move in validMoves:
        if square is move[0]:
            directions = move[1]
            
    # get the indicies of the passed in square
    for row, rows in enumerate(board):
        if square in rows:
            x = row
            y = rows.index(square)


    if square is board[x][y]:
        # For each direction where pieces can be flanked
        for direction in directions:
            zx = x
            zy = y

            # Flip all pieces to the left between square and a piece of the same color
            if direction is 1:
                while True:
                    zy -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip pieces up and left
            elif direction is 2:
                while True:
                    zy -= 1
                    zx -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip pieces above this piece
            elif direction is 3:
                while True:
                    zx -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip pieces up and right
            elif direction is 4:
                while True:
                    zx -= 1
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip ieces to the right
            elif direction is 5:
                while True:
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip pieces down and right
            elif direction is 6:
                while True:
                    zx += 1
                    zy += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            #Flip pieces below this piece
            elif direction is 7:
                while True:
                    zx += 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])
            
            # Flip pieces down and left
            elif direction is 8:
                while True:
                    zx += 1
                    zy -= 1
                    if board[zx][zy][1] is turn:
                        break
                    else:
                        flipPiece(board[zx][zy])

# Flip and individual piece
def flipPiece(square):

    if square[1] is not "e" and square[1] is not "h":
        if square[1] is "b":
            square[1] = "w"
        else:
            square[1] = "b"

# Print the board to the console    
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

# Redraw the screen
def updateBoard():

    # Wipe the screen
    screen.fill(BLACK)

    # Draw the board and pieces
    drawBoard(gameBoard, boardBackground)

    # Draw text elements on the screen
    drawText(screen)
    
    # Update the displaly
    pygame.display.flip()

# If one of the players has no moves left, press f to forefeit the turn
def forefeitTurn(screen):
    
    if turn is player1Color:
        setBottomText("Player 1 no moves. Press F to continue.", screen)
        print "Player 1 has no moves."
    else:
        setBottomText("Player 2 no moves. Press F to continue.", screen)
        print "Player 2 has no moves."

    updateBoard()

    # Do nothing until f is pressed
    while True:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                if event.key is pygame.K_f:
                    updateTurn()
                    updateBoard()
                    return

# Check if the game is over
def checkGameOver(board):

    global turn
    originalTurn = turn

    turn = "b"
    blackValidMoves = getValidSpaces(board)

    turn = "w"
    whiteValidMoves = getValidSpaces(board)

    # If neither player has valid moves from the current board state the game is over
    if len(whiteValidMoves) is 0 and len(blackValidMoves) is 0:
        turn = originalTurn
        return True
    else:
        turn = originalTurn
        return False

# Get the index values for an item in a 2d list
def index2D(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

# AI implementing minimax with Alpha Beta Pruning to play Othello
class Othello_AI:

    # Construct AI with how many levels deep to probe and the initial board state
    def __init__(self, levelsDeep, board):
        self.levelsDeep = levelsDeep
        self.currentBoard = board

    # Generate children from a given node
    def generateChildren(self, node, currentLevel):

        global turn
        startingNodeTurn = turn
        spaceFound = False
        sourceBoard = node.data
        initialState = deepcopy(sourceBoard)
        move = None
       
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

                        # Get index of the square on the board
                        x, y = index2D(sourceBoard, square)
                        # Create data that represents the move
                        move = ((x,y), square[1])

                        flipLines(square, validMoves, sourceBoard)
                        spaceFound = True
                        break

            # Create a node with the new board state and add it to the current node's children
            newBoard = deepcopy(sourceBoard)

            # Create a new neode with the move and board state and add it to children
            childState = Node(newBoard, move)
            node.addChild(childState)

            # Reset source board
            for x in range(ROWS):
                for y in range(COLS):
                    sourceBoard[x][y][1] = initialState[x][y][1]

            spaceFound = False

        currentLevel += 1

        # If not max level continue generating tree
        if currentLevel is not self.levelsDeep:
            if turn is "b":
                turn = "w"

            else:
                turn = "b"

            for child in node.children:
                self.generateChildren(child, currentLevel)

        turn = startingNodeTurn

    # Minimax algorithm with AB pruning
    def minimax(self, node, level, alpha, beta, maximizingPlayer):

        # If this is a leaf node or game over state, run the heuristic
        if level is self.levelsDeep or self.detectGameOver(node.data) is True:
            self.runHeuristics(node)
            if DEBUG is True:
                print "Leaf Node"
                print "Heuristic Calculated. Move {} has a value of {}\n".format(node.move, node.heuristic)
            return node.heuristic

        # If node is for the maximizing player
        if maximizingPlayer:
            maxEval = float("-inf")
            for child in node.children:
                # Get the heuristic for each child
                eval = self.minimax(child, level + 1, alpha, beta, False)
                if DEBUG is True:
                    print "Maximizing Node"
                    print "Considering  child move {} with value {}. Current max value for move {} is: {}".format(child.move, child.heuristic, node.move, maxEval)
                # Use new heuristic if it's higher
                maxEval = max(maxEval, eval)
                if DEBUG is True:
                    print "Updated Maximum Value: {}\n".format(maxEval)
                # Update alpha with the new heuristic if it's higher
                alpha = max(alpha, eval)
                # if beta is <= alpha, prune remaining children
                if beta <= alpha:
                    if DEBUG is True:
                        print "Beta {} for is <= Alpha {} for Maximizing Node".format(beta, alpha)
                        print "Remaining children of {} Alpha-pruned.\n".format(node.move)
                    break
            # Parent node's value is equal to it's largest child
            node.heuristic = maxEval
            if DEBUG is True:
                print "Final Value for {}: {}\n".format(node.move, node.heuristic)
            return maxEval

        else:
            # Node for minimizing player
            minEval = float("inf")
            for child in node.children:
                # Evaluate each child
                eval = self.minimax(child, level + 1, alpha, beta, True)
                if DEBUG is True:
                    print "Minimizing Node"
                    print "Considering  child move {} with value {}. Current min value for move {} is: {}".format(child.move, child.heuristic, node.move, minEval)
                # Use new heuristic if it's lower
                minEval = min(minEval, eval)
                if DEBUG is True:
                    print "Updated Minimum Value: {}\n".format(minEval)
                # update beta if the new heuristic is lower
                beta = min(beta, eval)
                # If beta <= alpha, prune remaining children
                if beta <= alpha:
                    if DEBUG is True:
                        print "Beta {} is <= Alpha {} for Minimizing Node".format(beta, alpha)
                        print "Remaining children of {} Beta-pruned.\n".format(node.move)
                    break
            # Current node's heurisitc is its smallest child's
            node.heuristic = minEval
            if DEBUG is True:
                print "Final Value for {}: {}\n".format(node.move, node.heuristic)
            return minEval

    # Print the sequence of nodes considered for the final heuristic
    def printMoveSequence(self, node):
        print "{} {}".format(node.move, node.heuristic)
        
        if len(node.children) is not 0:
            for child in node.children:
                if child.heuristic is node.heuristic:
                    self.printMoveSequence(child)

    # Generate a tree for all valid board states from the current state and run minimax on it
    # Return the root node and the new board state that results from the chosen move
    def generateTree(self):
    
        # source is the first node
        global turn
        originalTurn = turn
        source = Node(self.currentBoard, "Source")

        # starting a level 0 of the tree
        level = 0
        
        self.generateChildren(source, level)

        if DEBUG is True:
            print "Starting board:"
            printBoard(source.data)

        nextMove = self.minimax(source, level, float("-inf"), float("inf"), True)

        if DEBUG is True:
            print "Final Move Sequence:"
            self.printMoveSequence(source)
            print
        
        for child in source.children:
            if nextMove is child.heuristic: 
                print "AI selected move {}".format(child.move)
                nextMove = child.data
                break

        if type(nextMove) is not list:
            nextMove = None

        
        turn = originalTurn
        return source, nextMove

    # Detect if the current board state satisfies the game over condition
    def detectGameOver(self, board):

        global turn
        global foundGameOver
        originalTurn = turn

        turn = "b"
        blackValidMoves = getValidSpaces(board)

        turn = "w"
        whiteValidMoves = getValidSpaces(board)

        if len(blackValidMoves) is 0 and len(whiteValidMoves) is 0:
            turn = originalTurn
            foundGameOver = True
            return True

        else:
            turn = originalTurn
            return False

    # Update AI's knowledge of the current board state
    def setCurrentBoardState(self, boardState):

        newBoard = deepcopy(boardState)

        for row in newBoard:
            for square in row:
                if square[1] is "h":
                    square[1] = "e"
        
        self.currentBoard = newBoard

    # Run four heuristic functions on the node and weight them dynamically
    # Depending on the current statge of the game
    def runHeuristics(self, node):
        # Calculate coin parity
        coinHeuristic = self.coinParityHeuristic(node.data)
        # Calculate Mobility
        mobilityHeuristic = self.mobilityHeuristic(node.data)
        # Calculate corners captured and potential corners to capture
        cornerHeuristic = self.cornerHeuristic(node.data)
        # Calculate stability of the board
        stabilityHeurisitc = self.stabliityHeuristic(node.data)

        # Weight values are adjusted dynamically based on board state.
        
        if foundGameOver is True:
            # Focus on getting coins if the game is close to ending
            weightedAverageHeuristic = 1.00*coinHeuristic + 0.00*mobilityHeuristic + 0.00*cornerHeuristic + 0.00*stabilityHeurisitc
        
        elif turnCount > 20:
            # Focus on board stability and corners in the mid-game
            weightedAverageHeuristic = 0.05*coinHeuristic + 0.10*mobilityHeuristic + 0.45*cornerHeuristic + 0.40*stabilityHeurisitc
        
        else:
            # Focus on mobility and stability early on
            weightedAverageHeuristic = 0.05*coinHeuristic + 0.45*mobilityHeuristic + 0.10*cornerHeuristic + 0.40*stabilityHeurisitc

        node.heuristic = weightedAverageHeuristic

    # Calculate heuristic based off of player scores
    def coinParityHeuristic(self, board):
        p1Score = 0
        p2Score = 0

        for row in board:
            for space in row:
                if space[1] is player1Color:
                    p1Score += 1
                elif space[1] is player2Color:
                    p2Score += 1
        
        maxPlayerScore = p2Score
        minPlayerScore = p1Score
        
        heuristic = 100 * (maxPlayerScore - minPlayerScore) / (maxPlayerScore + minPlayerScore)

        return heuristic
        
    # Calculate heuristic based on player mobility
    def mobilityHeuristic(self, board):
        
        global turn
        originalTurn = turn

        turn = player2Color
        moves = getValidSpaces(board)
        player2Mobility = len(moves)

        turn = player1Color
        moves = getValidSpaces(board)
        player1Mobility = len(moves)

        turn = originalTurn
        
        maxPlayerMobility = player2Mobility
        minPlayerMobility = player1Mobility

        if player2Mobility + player1Mobility is not 0:
            heuristic = 100 * (maxPlayerMobility - minPlayerMobility) / (maxPlayerMobility + minPlayerMobility)
        else:
            heuristic = 0
        
        return heuristic

    # Calculate heuristic based on corners captured and corners near capture
    def cornerHeuristic(self, board):
        
        global player1Color
        global player2Color
        global turn

        player1Corners = 0
        player2Corners = 0

        corners = [board[0][0], board[0][7], board[7][0], board[7][7]]

        
        originalTurn = turn
        if turn is "b":
            turn = "w"
        else:
            turn = "b"
        
        nextMoves = getValidSpaces(board)
        turn = originalTurn

        for space in corners:
            # Corner's are already captured
            if space[1] is "b" or space[1] is "w":
                if space[1] is player1Color:
                    player1Corners += 1
                
                elif space[1] is player2Color:
                    player2Corners += 1
            
            else:
                # check if remaining corners are potentially attainable
                for move in nextMoves:
                    if move[0] is space:
                        if move[0][1] is player2Color:
                            player2Corners += 0.5
                        elif move[0][1] is player1Color:
                            player1Corners += 0.5

        maxPlayerCorner = player2Corners
        minPlayerCorner = player1Corners
        
        if player2Corners + player1Corners is not 0:
            heuristic = 100 * (maxPlayerCorner - minPlayerCorner) / (maxPlayerCorner + minPlayerCorner)
        else:
            heuristic = 0

        return heuristic

    # Calculate the stability of the board state
    def stabliityHeuristic(self, board):
        
        stableSpaces = []
        unstableSpaces = []

        player1Stability = 0
        player2Stability = 0
        
        for x in range(ROWS):
            for y in range(COLS):

                # Only count spaces with discs on them
                if board[x][y][1] is not "e" and board[x][y][1] is not "h":
                    if self.checkStable(board, stableSpaces, x, y):
                        stableSpaces.append(board[x][y])
                    
                    elif self.checkUnstable(board, x, y):
                        unstableSpaces.append(board[x][y])
        
        # Add for every stable space, subtract for each unstable space
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
        
        maxPlayerStability = player2Stability
        minPlayerStability = player1Stability
        
        if player2Stability + player1Stability is not 0:
            heuristic = 100 * (maxPlayerStability - minPlayerStability) / (maxPlayerStability + minPlayerStability)
        else:
            heuristic = 0

        return heuristic

    # Check if the space at the passed-in coordinates on the board is unstable                
    def checkUnstable(self, board, x, y):
        
        # If piece can be taken in the next move it is unstable
        global turn
        originalTurn = turn
        if board[x][y][1] is "b":
            turn = "w"
        else:
            turn = "b"

        # Get the next moves
        moves = getValidSpaces(board)

        turn = originalTurn

        adjacentSpaces = []
        
        # Get all spaces next to the space in question
        if x in range(1,6):
            adjacentSpaces.append(board[x+1][y])
            adjacentSpaces.append(board[x-1][y])

        if y in range(1,6):
            adjacentSpaces.append(board[x][y+1])
            adjacentSpaces.append(board[x][y-1])

        if x in range(1,6) and y in range(1,6):
            adjacentSpaces.append(board[x-1][y-1])
            adjacentSpaces.append(board[x+1][y+1])
            adjacentSpaces.append(board[x-1][y+1])
            adjacentSpaces.append(board[x+1][y-1])

        # If one of the adjacent spaces is a valid move this space is unstable
        for space in moves:
            if space[0] in adjacentSpaces:
                return True
        
        return False
    
    # Check if the space at the coordinates is stable
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
            
            elif y in range(1,7):
                if board[x][y - 1] in stableSpaces or board[x][y + 1] in stableSpaces:
                    stableHor = True
        
        # check vertically
        # Piece is stable verticall if column is full
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
            
            elif x in range(1,7):
                if board[x - 1][y] in stableSpaces and board[x - 1][y] in board or board[x + 1][y] in stableSpaces and board[x + 1][y] in board:
                    stableVert = True
        
        # check diagonal axes the same way as horizontal and vertial
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
            
            elif x in range(1,7) and y in range(1,7):
                if board[x - 1][y - 1] in stableSpaces or board[x + 1][y + 1] in stableSpaces:
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
            
            elif x in range(1,7) and y in range(1,7):
                if board[x + 1][y - 1] in stableSpaces or board[x -1][y + 1] in stableSpaces:
                    stableDiagFront = True

        # If a piece is table in all directions then it is stable
        if stableHor and stableVert and stableDiagBack and stableDiagFront:
            return True
        else:
            return False

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

# Initalize AI
comp = Othello_AI(3, deepcopy(gameBoard))

drawBoard(gameBoard, boardBackground)
drawText(screen)
pygame.display.flip()

validMoves = getValidSpaces(gameBoard)

# Main game loop
done = False
while not done:
    
    # Main events loop
    

    # If a human player has no moves left
    if (turn is player1Color or turn is player2Color and compActive is False) and len(validMoves) is 0:
        # Check if a game over state has been reached
        if checkGameOver(gameBoard) is True:
            gameOver = True
            if player1Score > player2Score:
                setBottomText("Player 1 Wins!", screen)
            
            else:
                if compActive is True:
                    setBottomText("The AI has won.", screen)
                
                else:
                    setBottomText("Player 2 Wins!", screen)
                
            updateBoard()
        
        # Otherwise the player forefeits their turn
        else:
            forefeitTurn(screen)

    
    
    for event in pygame.event.get():
        # If the x button on the window is clicked, end the game
        if event.type is pygame.QUIT:
            done = True

        # If the d key is pressed enable debug mode for minimax
        if event.type is pygame.KEYDOWN:
            if event.key is pygame.K_d:
                if DEBUG is True:
                    print "Debug off.\n"
                    DEBUG = False
                
                else:
                    print "Debug on.\n"
                    DEBUG = True

        # If the mouse moves or is clicked
        if (compActive is False or compActive is True and turn is player1Color) and gameOver is False:
            if event.type is pygame.MOUSEMOTION or event.type is pygame.MOUSEBUTTONUP:
                # Get the mouse's position
                pos = pygame.mouse.get_pos()
                
                # For each square on the board
                for row in gameBoard:
                    for square in row:
                        # If the mouse is over the square and the square is empty
                        if square[0].collidepoint(pos) and square[1] is not "b" and square[1] is not "w":
                            # If the mouse moved, and if the space is valid, highlight the square
                            if event.type is pygame.MOUSEMOTION:
                                for move in validMoves:
                                    if square is move[0]:
                                        square[1] = "h"
                            
                            # if it was a click place a piece
                            elif event.type is pygame.MOUSEBUTTONUP and square[1] is "h":
                                
                                flipLines(square, validMoves, gameBoard)
                                
                                square[1] = turn

                                printBoard(gameBoard)
                                print
                                comp.setCurrentBoardState(gameBoard)
                                
                                updateTurn()
                                validMoves = getValidSpaces(gameBoard)
                                
                                # Update the score
                                updateScore()
                                updateBoard()
            
                        # Un-highlight any square the mouse doesn't touch or isn't valid
                        elif square[1] is "h":
                            square[1] = "e"
        
        elif compActive is True and turn is player2Color and gameOver is False:
            # AI turn
            # Generate new tree
            print "AI is thinking...\n"
            sleep(1)
            decisionTree, nextMove = comp.generateTree()
            # Make the best move
            if nextMove is not None:
                print "AI Move"
                printBoard(nextMove)
                print
                # Set gameBoard to AI's new move
                gameBoard = deepcopy(nextMove)
                # Update the board state for the AI
                comp.setCurrentBoardState(gameBoard)
                
                updateTurn()
                validMoves = getValidSpaces(gameBoard)
                updateScore()
                updateBoard()
            
            else:
                # AI forefiets their turn if it has no moves
                print "AI found no moves."
                updateTurn()
                validMoves = getValidSpaces(gameBoard)
                # Update the score
                updateScore()
                updateBoard()
    updateBoard()