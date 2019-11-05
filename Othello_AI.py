import Node

class Othello_AI:

    # Requirements:
    # Easily adjustable search depth
    # Computer can play white or black
    # Debug mode that prints out sequences of moves considered from current state with associated heuristic value
    # Debug can be toggled on a move by move basis
    # Debug mode that indicates when a branch is pruned and which branch is pruned
    # Implements mini-max
    # Implements alpha-beta pruning

    def __init__(self, levelsDeep, currentBoardState):
        self.levelsDeep = levelsDeep
        self.currentBoardState = currentBoardState
        self.maxPlayerScore = 0;

    def generateTree(self):
        pass

    def setCurrentBoardState(self, newBoardState):
        self.currentBoardState = newBoardState

    def getBoardData(self):
        # Calculate player coin parities
        
        # Calculate player mobilities
        # Calculate corners captured
        # Calculate player stability

        pass

    def runHeuristics(self, node):
        # Calculate coin parity
        # Calculate Mobility
        # Calculate number of corners captured
        # Calculate stability

        pass

    def coinParityHeuristic(self):
        pass

    def mobilityHeuristic(self):
        pass

    def cornerHeuristic(self):
        pass

    def stabliityHeuristic(self):
        pass