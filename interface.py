from board import *
from pieces import *

def interfaceLoop():
    if input("Would you like to play a game of chess? Answer 'y'/'n'.\n"):
        b = Board()
        b.resetBoard()
        
        # Following are used to track the state of black and white kings
        whiteKing = b.state[7][4]
        blackKing = b.state[0][4]

        # Default turn is white
        turn = "white"
        
        # While neither king is captured, primary gameplay loop continues
        while whiteKing.alive and blackKing.alive:
            b.turnCount += 1
            if turn == "white":
                print("White's turn.\n")
            else:
                print("Black's turn.\n")
            
            print(b)

            # Obtaining desired piece to move
            rowChoice = -1
            colChoice = -1
            while True:
                rowChoice = int(input("Choose a piece first by row: "))
                colChoice = int(input("Choose a piece second by column: "))
                print()
                if b.inBounds(rowChoice, colChoice):
                    break
                print("Please choose a valid tile.")

            possibleMoves = []

            # If the chosen tile seats an allied piece
            if b.isAlly(turn, rowChoice, colChoice):
                allyObject = b.state[rowChoice][colChoice]

                if type(allyObject) == Rook or type(allyObject) == Queen:
                # Note that you must add castling-capability
                    print(type(allyObject), " identified.\n")

                    # We add valid rook moves to possibleMoves
                    Rook.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                
                if type(allyObject) == Bishop or type(allyObject) == Queen:
                    print(type(allyObject), " identified.\n")

                    # We add valid bishop moves to possibleMoves
                    Bishop.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                
                elif type(allyObject) == Chevalier:
                    print(type(allyObject), " identified.\n")

                    Chevalier.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)

                elif type(allyObject) == Pawn:
                # Note that you must add ability to upgrade pawns
                    print(type(allyObject), " identified.\n")
                    
                    # We add valid pawn moves to possibleMoves
                    Pawn.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)

                elif type(allyObject) == King:
                    print(type(allyObject), " identified.\n")

                    # We add valid king moves to possibleMoves
                    King.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)

                # If there are possible moves for given piece proceeds; elsewise, restarts loop
                if not possibleMoves:
                    print("Please choose a different piece.\n")
                    continue
                
                # Calls board method to create graph of possiblities and then prints it
                print(b.possibilitiesGraph(possibleMoves))

                # Calls board method to confirm choice to move piece
                # Compares target to possible moves and uses rowChoice and colChoice to set origin to be empty
                if b.getMove(possibleMoves, rowChoice, colChoice):
                    print(b)
                else: # If player rejects choice
                    print("Please choose a different piece.\n")
                    continue
            
            # If player chooses invalid tile, choice loop restarts
            else:
                print("Invalid choice. Please choose again.\n")
                continue

            # Turn alternator; comes at the very end after a successful move by the previous player
            if turn == "white":
                turn = "black"
            else:
                turn = "white"
        
        # Win statements
        if not whiteKing.alive:
            print("Black wins on turn " + str(b.turnCount) + ".")
        if not blackKing.alive:
            print("White wins on turn " + str(b.turnCount) + ".")

interfaceLoop()