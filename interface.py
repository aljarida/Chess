from board import *
from pieces import *
from graveyard import *

def interfaceLoop():
    # We create the board object and set it
    b = Board()
    b.resetBoard()

    if b.fancyPrint("Would you like to play a game of chess? Answer 'y'/'n': ", inp=True) == 'y':
        print()

        # We create white and black graveyards
        whiteGrave, blackGrave = Graveyard("white"), Graveyard("black") 

        # Following are used to track the state of black and white kings
        whiteKing, blackKing = b.state[7][4], b.state[0][4]

        # Default turn is white
        turn = "white"
        
        # While neither king is captured, primary gameplay loop continues
        while whiteKing.alive and blackKing.alive:
            b.turnCount += 1
            if turn == "white":
                b.fancyPrint("White's turn.\n")
                enemyGrave = blackGrave
            else:
                b.fancyPrint("Black's turn.\n")
                enemyGrave = whiteGrave
            
            print(b)

            # Obtaining desired piece to move
            chosenMoves = b.getMove([whiteGrave, blackGrave])
            rowChoice, colChoice = chosenMoves[0], chosenMoves[1]

            possibleMoves = []
            # If the chosen tile seats an allied piece
            if b.isAlly(turn, rowChoice, colChoice):
                allyObject = b.state[rowChoice][colChoice]
                allyType = type(allyObject)
                # If piece is Queen, add Rook's and Bishop's moves both
                if allyType.__name__ == "Queen":
                    Rook.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                    Bishop.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                # Otherwise, grab the piece's specific moves by evaluating class name to grab its respective method
                else:
                    eval(allyType.__name__).moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                
                # Print selected piece name
                b.fancyPrint(allyType.__name__ + " identified.\n")

                # If there are possible moves for given piece proceeds; elsewise, restarts loop
                if not possibleMoves:
                    b.fancyPrint("Piece has no valid moves. Choose a different piece.\n")
                    continue
                
                # Calls board method to create graph of possiblities and then prints it
                print(b.possibilitiesGraph(possibleMoves))

                # Calls board method to confirm choice to move piece
                # Compares target to possible moves and uses rowChoice and colChoice to set origin to be empty
                if not b.commitMove(possibleMoves, rowChoice, colChoice, enemyGrave):
                    b.fancyPrint("Please choose a different piece.\n") # If player rejects choice
                    continue
            
            # If player chooses invalid tile, choice loop restarts
            else:
                b.fancyPrint("Invalid choice. Please choose again.\n")
                continue

            # Turn alternator; comes at the very end after a successful move by the previous player
            if turn == "white":
                turn = "black"
            else:
                turn = "white"
        
        # Win statements
        if not whiteKing.alive:
            b.fancyPrint("Black wins on turn " + str(b.turnCount) + ".")
        if not blackKing.alive:
            b.fancyPrint("White wins on turn " + str(b.turnCount) + ".")

interfaceLoop()