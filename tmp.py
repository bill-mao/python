




# 父亲board 指针int， queue 的index
class Board:
    def __init__():




def ramGenerate():

    return board


# encode int 
def enc(board):

    code
    return (code, father)

# decode 棋盘
def dec(code):

    return board

# next move; 
# don't move the previous pawn! 
def move(board, prePawn):

    # stop move the same pawn

    # del exits board
    if not exits():
        append


    return boards, codes

def exits(code):

    # found before?

    # exits a mirror?



    return True


def gameover(board):

    return False


def printResult():
    pass


if __name__ == '__main__':
    # like (int, int father_point)
    queue = []
    iniBoard = ramGenerate()
    queue.append(enc(iniBoard))
    cur = 0

    # BFS search
    while cur<len(queue):
        curBoard = decode(queue[cur])
        sonBoards, sonCodes = move(curBoard)
        for sb, sc in sonBoards, sonCodes:
            if gameover(sb):
                printResult(sc)
            else:
                queue.append(sc)
        cur+=1
    if cur == len(queue):
        print('there's no solution')



