import time
from collections import Counter

from pieces import *

class Board:
    def __init__(self):
        # Initializing empty 8x8 board composed of "__" strings
        self.state = [["___"]*8 for _ in range(8)]
        # Initializing turn counter
        self.turnCount = 1
    
    # Creating string representation of grid with row and column labels
    def __repr__(self):
        repr = "\n"
        rowNum = 8
        for row in self.state:
            repr += str(rowNum) + " |"
            rowNum -= 1
            for tile in row:
                repr += " " + str(tile) + " |" # Casts the tile (the pieces' objects or placeholder "___") into a string
            repr += "\n"
        repr += "     A     B     C     D     E     F     G     H\n"
        return repr
    
    # Method for printing text and inputs in a visually interesting manner
    def fancyPrint(self, str, latency=0.01, inp=False, end=None):
        for c in str:
            print(c, end="", flush=True)
            time.sleep(latency)
        if inp:
            return input()
        elif end != "":
            print()

    # Creates board to standard chess specifications
    def resetBoard(self):
        # Creates an empty board to fill in
        self.state = [["___"]*8 for _ in range(8)]

        def placePieces(color):
            if color == "white":
                row = 7 # Used to place non-Pawn pieces
                dif = -1 # Used to modify row later to place Pawns
            else: # "Black"
                row = 0
                dif = 1
            
            # Setting Bishops
            self.state[row][2] = Bishop(color, [row, 2])
            self.state[row][5] = Bishop(color, [row, 5])

            #Setting Chevaliers
            self.state[row][1] = Chevalier(color, [row, 1])
            self.state[row][6] = Chevalier(color, [row, 6])

            # Setting Rooks
            self.state[row][0] = Rook(color, [row, 0])
            self.state[row][7] = Rook(color, [row, 7])

            # Setting King/Queen
            self.state[row][3] = Queen(color, [row, 4])
            self.state[row][4] = King(color, [row, 3])

            row += dif
            # Setting Pawns
            for col in range(8):
                self.state[row][col] = Pawn(color, [row, col])
            
        # Process to set both colors
        for color in ["black", "white"]:
            placePieces(color)
    
    # Creates a copy of the current board with a board object but with only strings
    # Called with argument array (moves) to represent those possible moves on the board
    def possibilitiesGraph(self, moves):
        copyBoard = Board()

        # Copies string representations of current board pieces over
        for row in range(8):
            for col in range(8):
                copyBoard.state[row][col] = str(self.state[row][col])
        
        # Marks possibilities with "_?_" or "_!_"
        for move in moves:
            # moves[0] == row & move[1] == col
            currentRep = copyBoard.state[move[0]][move[1]]
            if currentRep == "___": # If empty tile
                copyBoard.state[move[0]][move[1]] = "_?_"
            else: # If enemy piece
                copyBoard.state[move[0]][move[1]] = currentRep[0] + "!" + currentRep[2]
        
        return copyBoard
    
    """ Method to read input from user to dictate move. Accepts inputs between A-H and a-h (equally) for columns
        and inputs between 1-8 for rows, and translates the input into grid/row indices for the engine to interpret.
        Input can be any 1 character and 1 integer within the valid ranges with any number of white space.
        Accepts the optional argument graves which when True enables the user to print the current graveyards.
    """
    def getMove(self, graves=False):
        rowChoice, colChoice = -1, -1
        while True:
            # Character-translation dictionary
            letterToNum = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
            # Allowable numerical entries
            validNums = ('1', '2', '3', '4', '5', '6', '7', '8')
            
            # Requests input from user and remove white space
            if graves:
                moveInput = self.fancyPrint("Enter a valid letter-number combination (or '0' to view graveyards): ", inp=True).replace(" ", "")
            else:
                moveInput = self.fancyPrint("Enter a valid letter-number combination: ", inp=True).replace(" ", "")
            # Removes redundant repeated entries and separates characters into list
            charSet = set()
            for char in moveInput.upper():
                charSet.add(char)
            moveInput = list(charSet)

            # Checks for valid length and parses input
            if len(moveInput) == 2:
                # Performs coordinate translation duties
                for char in moveInput:
                    if char in letterToNum:
                        colChoice = letterToNum[char]
                    elif char in validNums:
                        rowChoice = 8 - int(char)
                # Checks that translated coordinates are valid
                if self.inBounds(rowChoice, colChoice):
                    return [rowChoice, colChoice]
            # If input is '0' and graves=True, prints White's and Black's graves
            elif graves and moveInput[0] == '0':
                print(graves[0], graves[1])
            # While there is no valid input, loop continues
            self.fancyPrint("Please choose a valid tile.")

    # Asks player if they would like to proceed
    # If yes, player chooses a tile to move to
    def commitMove(self, possibleMoves, rowChoice, colChoice, enemyGrave):
        if input("Move this piece? Answer 'y'/'n': ") == 'y':
            while True:
                moveCoords = self.getMove()
                if moveCoords in possibleMoves:
                    self.movePiece([rowChoice, colChoice], moveCoords, enemyGrave)
                    return True
                self.fancyPrint("Please choose a valid tile.")
        return False
    
    # Moves a piece to a target by taking in coordinates for both
    def movePiece(self, origin, target, enemyGrave):
        originPiece = self.state[origin[0]][origin[1]] # Acquiring object data at origin (row, col)
        targetPiece = self.state[target[0]][target[1]] # Acquiring data at target (row, col)
        
        # The target King is removed, thus we set it as not alive
        if type(targetPiece) == King:
            targetPiece.alive = 0
        
        # The origin Pawn moves, thus we mark that it has already made its first move
        if type(originPiece) == Pawn:
            originPiece.firstMove = 0

            # We check for a two-tile advance to establish en passant vulnerability and mark the turn it was made
            if abs(target[0] - origin[0]) == 2:
                originPiece.enPassantVulnerable = self.turnCount
            
            # If a pawn can diagonally move to an empty tile, we know it is en passant
            if targetPiece == "___":
                self.state[origin[0]][target[1]] = "___" # We remove the enemy pawn
        
            # If a pawn crosses into the final row, promotion is required
            if (target[0] == 0) or (target[0] == 7):
                self.fancyPrint("Choose a promotion from the following options.")
                ranks = ["Queen","Rook","Bishop","Chevalier"]
                for i, rank in enumerate(ranks):
                    print(str(i) + ". " + rank)
                print()
                rankChoice = -1
                while rankChoice not in [0,1,2,3]:
                    rankChoice = int(self.fancyPrint("Enter an associated number to proceed: ", inp=True))
                originPiece = eval(ranks[rankChoice])(originPiece.color, [origin[0]][origin[1]])
                self.fancyPrint("\nYour Pawn has been promoted to a " + ranks[rankChoice])
        
        # Adding string representation of removed piece to grave
        if targetPiece != "___":
            enemyGrave.grave.append(str(targetPiece))
        # Replacing target's destination with piece object
        self.state[target[0]][target[1]] = originPiece
        # Replacing piece's former destination with placeholder string
        self.state[origin[0]][origin[1]] = "___"
    
    # Checks that the chosen coordinates are in bounds
    def inBounds(self, row, col):
        return -1 < row < 8 and -1 < col < 8

    # Checks that the chosen piece is in bounds and IS an empty tile
    def isString(self, row, col):
        return self.inBounds(row, col) and type(self.state[row][col]) == str

    # Checks that the chosen piece is in bounds and NOT an empty tile
    def notString(self, row, col):
        return self.inBounds(row, col) and type(self.state[row][col]) != str
    
    # Checks that the chosen piece is in bounds, not a string, and of SAME color
    def isAlly(self, turn, row, col):
        return self.notString(row, col) and self.state[row][col].color == turn
    
    # Checks that the chosen piece is in bounds, not a string, and of OPPOSITE color
    def isEnemy(self, turn, row, col):
        return self.notString(row, col) and self.state[row][col].color != turn