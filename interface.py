import time

from board import *
from pieces import *
from graveyard import *

def interfaceLoop():
    b = Board() # Creates the Board object
    b.resetBoard() # Sets the Board object

    if b.fancyPrint("Would you like to play a game of chess? Answer 'y'/'n': ", inp=True) == 'y':
        # Creates White's and Black's graveyards
        whiteGrave, blackGrave = Graveyard("white"), Graveyard("black") 
        # References stored to King objects to track their states (in play or removed)
        whiteKing, blackKing = b.state[7][4], b.state[0][4]

        # Creates timers to track durations of play
        # turnTimes[0] is Black's time; turnTimes[1] is White's time
        turnTimes = [0, 0]
        currentTime = time.time()
        
        # While neither king is captured, primary gameplay loop continues
        while True:
            # If turn count is NOT even, is White's turn
            if b.turnCount % 2 == 1:
                turn = "white"
                enemyGrave, enemyKing = blackGrave, blackKing
            
            # If turn count IS even, is Black's turn
            else:
                turn = "black"
                enemyGrave, enemyKing = whiteGrave, whiteKing
            
            # Prints Board object
            print(b)

            # Prints turn
            b.fancyPrint(turn.capitalize() + "'s turn.")

            # Obtaining desired piece to move
            chosenMoves = b.getMove(graves=[whiteGrave, blackGrave])
            rowChoice, colChoice = chosenMoves[0], chosenMoves[1]

            # If the chosen tile seats an allied piece
            if b.isAlly(turn, rowChoice, colChoice):
                allyObject = b.state[rowChoice][colChoice]
                allyType = type(allyObject)
                possibleMoves = []

                # If piece is Queen, add Rook's and Bishop's moves both
                if allyType.__name__ == "Queen":
                    Rook.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
                    Bishop.moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)

                # Otherwise, grab the piece's specific moves by evaluating class name to grab respective method
                else:
                    eval(allyType.__name__).moves(allyObject, b, turn, rowChoice, colChoice, possibleMoves)
            
                # If there are possible moves for given piece, proceeds
                if possibleMoves:
                    # Calls board method to create graph of possiblities and then prints it
                    print(b.possibilitiesGraph(possibleMoves))

                    # Prints chosen piece name
                    b.fancyPrint(allyType.__name__ + " identified.")

                    # Calls board method to confirm choice to move piece
                    if b.commitMove(possibleMoves, rowChoice, colChoice, enemyGrave):
                        # Updates turn time for respective turn color
                        turnTimes[b.turnCount % 2] += time.time() - currentTime
                        # Updates time for next-turn time-tracking
                        currentTime = time.time()

                        # If move confirmed, turn increments
                        b.turnCount += 1
                        # Win condition and statement, breaks out of entire game loop
                        if not enemyKing.alive:
                            print(b)
                            b.fancyPrint(turn.capitalize() + " wins on turn " + str(b.turnCount) + ".")
                            # Prints timer statistics
                            b.fancyPrint("Game lasted " + str(round(int(sum(turnTimes)/60), 3)) + " minutes.")
                            for i, turn in enumerate(["White","Black"]):
                                b.fancyPrint(turn + " accumulated " + str(round(turnTimes[1 - i]/60, 3)) + " minutes of turn time. ")
                            break

                    # If players disconfirms move, loop restarts and asks player to choose another piece
                    else:
                        b.fancyPrint("Please choose a different piece.\n")
                        continue

                # If piece has no possible moves, loop restarts and asks player to choose another piece
                else:
                    b.fancyPrint(allyType.__name__ + " has no valid moves. Please choose a different piece.\n")
                    continue
                
            # If player chooses invalid tile, loop restarts and asks player to choose another piece
            else:
                b.fancyPrint("Invalid choice. Please choose a different tile.\n")
                continue

interfaceLoop()