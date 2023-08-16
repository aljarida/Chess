from board import *

class Pawn:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.firstMove = 1
        self.enPassantVulnerable = 0

    def moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves):
        # Direction pawn is moving
        if turn == "white":
                heading = -1 # Up if white
        else:
            heading = 1 # Down if black

        # Scans three columns ahead of pawn in correct direction
        for col in range(colChoice-1, colChoice+2):
            if col == colChoice:
                # If the move directly ahead is empty (i.e., a string)
                if b.isString(rowChoice + heading, col):
                    possibleMoves.append([rowChoice + heading, col])
            # For diagonal possibilities
            else:
                # If the diagonal tile is an enemy
                if b.isEnemy(turn, rowChoice + heading, col):
                    possibleMoves.append([rowChoice + heading, col])
                # If the diagonal is empty but an enemy lies behind it
                elif b.isEnemy(turn, rowChoice, col):
                    tileBehind = b.state[rowChoice][col]
                    if (type(tileBehind) == Pawn) and (tileBehind.enPassantVulnerable == b.turnCount-1):
                        possibleMoves.append([rowChoice + heading, col])
            
        # Scanning for possible first-move extra movement
        if allyObject.firstMove and b.isString(rowChoice + heading*2, colChoice):
                possibleMoves.append([rowChoice + heading*2, colChoice])

    def __repr__(self):
        return self.color[0] + "_P"

class Rook:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords

    def moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves):
        for index in [0, 1]: # First modifies row, then col
            for sign in [1, -1]: # First moves down/right, then up/left
                tempCoords = [rowChoice, colChoice]
                tempCoords[index] += (1*sign) # Increments
                
                # Checks for enemy or empty tile
                while b.isString(tempCoords[0], tempCoords[1]) or b.isEnemy(turn, tempCoords[0], tempCoords[1]):
                    possibleMoves.append([tempCoords[0], tempCoords[1]])
                    if b.isEnemy(turn, tempCoords[0], tempCoords[1]):
                        break # First enemy encountered breaks loop
                    tempCoords[index] += (1*sign)
    
    def __repr__(self):
        return self.color[0] + "_R"
    
class Chevalier:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords

    def moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves):
        movements = [[1, 2], [2, 1]]
        for movement in movements:
            for sign1 in [1, -1]:
                for sign2 in [1, -1]:
                    jumpRow = rowChoice + movement[0]*sign1
                    jumpCol = colChoice + movement[1]*sign2
                    if b.isString(jumpRow, jumpCol) or b.isEnemy(turn, jumpRow, jumpCol):
                        possibleMoves.append([jumpRow, jumpCol])

    def __repr__(self):
        return self.color[0] + "_C"
    
class Bishop:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
    
    def moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves):
        increments = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for increment in increments:
            diagonalRow = rowChoice + increment[0]
            diagonalCol = colChoice + increment[1]
            while b.isString(diagonalRow, diagonalCol) or b.isEnemy(turn, diagonalRow, diagonalCol):
                possibleMoves.append([diagonalRow, diagonalCol])
                if b.isEnemy(turn, diagonalRow, diagonalCol):
                    break
                diagonalRow += increment[0]
                diagonalCol += increment[1]

    def __repr__(self):
        return self.color[0] + "_B"
    
class Queen:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
    
    def __repr__(self):
        return self.color[0] + "_Q"

class King:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.alive = True

    def moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves):
        adjacentMods = [[1, 1], [1, 0], [1, -1], # Tiles ahead
                        [0, 1], [0, -1], # Tiles to sides
                        [-1, 1], [-1, 0], [-1, -1]] # Tiles behind
                    
        for mod in adjacentMods:
            kingRow = rowChoice + mod[0]
            kingCol = colChoice + mod[1]
            if b.isString(kingRow, kingCol) or b.isEnemy(turn, kingRow, kingCol):
                possibleMoves.append([kingRow, kingCol])

    def __repr__(self):
        return self.color[0] + "_K"