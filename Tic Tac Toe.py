#printing the game board
board = ["_","_","_",
         "_","_","_",
         "_","_","_"]
currentPlayer = "X"
winner = None
gameRunning = True

#print game board
def printborad(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--------------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--------------")
    print(board[6] + " | " + board[7] + " | " + board[8])

print(board)

#take player input
def inputPlayer(board):
    int_user = int(input("Enter a number 1-9: "))
    if int_user >= 1 and int_user <= 9 and board[int_user-1] =="_":
        board[int_user-1]=currentPlayer
    else:
        print("Oops pleayer is alredy in that spot")

#check for win or tie
def checkhorizontal(board):
    global winner
    if board[0] == board[1] == board[2] and board[1] != "_":
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != "_":
        winner == board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != "_":
        winner == board[6]
        return True
def checkrow(board):
    global winner
    if board[0] == board[3] == board[6] and board[0] != "_":
        winner = board[0]
        return True
    elif board[1] == board[4] == board[7] and board[1] != "_":
        winner == board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != "_":
        winner == board[2]
        return True
def checkdiaglog(board):
    global winner
    if board[0] == board[4] == board[8] and board[0] != "_":
        winner = board[0]
        return True
    elif board[2] == board[4] == board[6] and board[2] != "_":
        winner == board[2]
        return True
def checkTie(board):
    global gameRunning
    if "_" not in board:
        printborad(board)
    print("it is a tie")
    gameRunning = False

def checkWin():
    if checkdiaglog(board) or checkrow(board) or checkhorizontal(board):
        print(f"The winner is {winner}")
#swtich the player

def switchPlayer():
    global currentPlayer
    if currentPlayer == "X":
        currentPlayer = "O"
    else:
        currentPlayer = "X"

#check win or tie again
while gameRunning:
    printborad(board)
    if winner != None:
        break
    inputPlayer(board)
    checkWin()
    checkTie(board)
    switchPlayer()

