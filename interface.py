from board import *
from pieces import *
from graveyard import *

def interfaceLoop():
    b = Board() # We create the Board object
    b.resetBoard() # We set it

    if b.fancyPrint("Would you like to play a game of chess? Answer 'y'/'n': ", inp=True) == 'y':

        # We create white and black graveyards
        whiteGrave, blackGrave = Graveyard("white"), Graveyard("black") 

        # References stored to King objects to track states
        whiteKing, blackKing = b.state[7][4], b.state[0][4]
        
        # While neither king is captured, primary gameplay loop continues
        while whiteKing.alive and blackKing.alive:
            # If turn count is NOT even, it is White's turn
            if b.turnCount % 2 == 1:
                turn = "white"
                enemyGrave = blackGrave
            # Otherwise it is Black's turn
            else:
                turn = "black"
                enemyGrave = whiteGrave
            
            # Printing the board
            print(b)

            # Printing turn
            b.fancyPrint(turn.capitalize() + "'s turn.")

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
                # Otherwise, grab the piece's specific moves by evaluating class name to grab respective method
                else:
                    eval(allyType.__name__).moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
            
                # If there are possible moves for given piece proceeds
                if possibleMoves:
                    # Calls board method to create graph of possiblities and then prints it
                    print(b.possibilitiesGraph(possibleMoves))

                    # Print chosen piece name
                    b.fancyPrint(allyType.__name__ + " identified.")

                    # Calls board method to confirm choice to move piece
                    if b.commitMove(possibleMoves, rowChoice, colChoice, enemyGrave):
                        # If move confirmed, turn increments
                        b.turnCount += 1
                    # Otherwise restarts selection loop
                    else:
                        b.fancyPrint("Please choose a different piece.\n") # If player rejects choice
                        continue
                # If there are no possible moves for a given piece, asks user to select different piece
                else:
                    b.fancyPrint(allyType.__name__ + " has no valid moves. Please choose a different piece.\n")
                    continue
                
            # If player chooses invalid tile, choice loop restarts
            else:
                b.fancyPrint("Invalid choice. Please choose again.\n")
                continue
        
        # Win conditions and statements
        if not whiteKing.alive:
            b.fancyPrint("Black wins on turn " + str(b.turnCount) + ".")
        if not blackKing.alive:
            b.fancyPrint("White wins on turn " + str(b.turnCount) + ".")

interfaceLoop()