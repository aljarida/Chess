from pieces import *

class Board:
    def __init__(self):
        # Initializing empty 8x8 board composed of __'s
        self.state = [["___"]*8 for _ in range(8)]
        # Initializing turn counter
        self.turnCount = 0
    
    # Creating string representation of grid with row and column numerical labels
    def __repr__(self):
        repr = ""
        col = 0
        for row in self.state:
            repr += str(col) + " |"
            col += 1
            for tile in row:
                repr += " " + str(tile) + " |" # Casts the tile (the pieces' objects or placeholder "___") into a string
            repr += "\n"
        repr += "     0     1     2     3     4     5     6     7\n"
        return repr

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
        # "!" indicates option for removal of enemy piece
        for move in moves:
            # moves[0] == row & move[1] == col
            currentRep = copyBoard.state[move[0]][move[1]]
            if currentRep == "___":
                copyBoard.state[move[0]][move[1]] = "_?_"
            else:
                copyBoard.state[move[0]][move[1]] = currentRep[0] + "!" + currentRep[2]
        
        return copyBoard

    # Asks player if they would like to proceed
    # If yes, player chooses a tile to move to
    def getMove(self, possibleMoves, rowChoice, colChoice):
        if input("Move this piece? Answer 'y'/'n'.\n") == 'y':
            while True:
                moveCoords = []
                moveRow = int(input("Choose a target tile first by row: "))
                moveCol = int(input("Choose a target tile second by column: "))
                print()
                moveCoords.append(moveRow)
                moveCoords.append(moveCol)
                if moveCoords in possibleMoves:
                    self.movePiece([rowChoice, colChoice], moveCoords)
                    return True
                print("Please choose a valid tile.")
        return False
    
    # Moves a piece to a target by taking in coordinates for both
    def movePiece(self, origin, target):
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
                print("Choose a promotion from the following options.")
                ranks = ["Queen","Rook","Bishop","Chevalier"]
                for i, rank in enumerate(ranks):
                    print(str(i) + ". " + rank)
                print()
                rankChoice = -1
                while rankChoice not in [0,1,2,3]:
                    rankChoice = int(input("Enter an associated number to proceed: "))
                originPiece = eval(ranks[rankChoice])(originPiece.color, [origin[0]][origin[1]])
                print("\nYour Pawn has been promoted to a" + ranks[rankChoice])
        
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