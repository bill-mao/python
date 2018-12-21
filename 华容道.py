


# 关键board的格式，在这个格式之下怎么move方便

# 父亲board 指针int， queue 的index
class Board:
    '''保存华容道棋盘类
    '''
    def __init__(pos, blankspace, prePawn,  ):
        '''[summary]
        
        [description]
        封装对象不需要知道额外的信息
        Arguments:
            depth {int} -- 当前遍历深度
            fatherIndex {int} -- 数组的，或者字符串的位置
            blankspace {tuple} -- 未定，大概是空格的位置; 从小到大
            pos {数组还是字符串？} -- 从左到右从上到下编码
                空格 0
                小兵 1
                横将 2
                竖将 3 
                曹操 4
                    只编码左上角的，其余统一使用-1 或者任意数字, 按照顺序不会干扰？

            0  1  2  3 
            4  5  6  7 
            8  9  10 11 
            12 13 14 15 
            16 17 18 19 
        '''
        self.depth = depth
        self.father = fatherIndex
        self.prePawn = prePawn
        self.blankspace = blankspace
        self.pos = pos

    def gameover(self):
        if 4 ==self.pos[13]==self.pos[14]==self.pos[17]==self.pos[18]:
            return True
        else: return False



    # next move; 
    # don't move the previous pawn! 
    def nextMove(self):
        




        # 两个空格相连
        # 兵可以走两个空格，可以拐弯，算一步
        # else可以移动一格
        b = self.blankspace[0]
        bb = self.blankspace[1]
        pos = self.pos 
        out = []

        # directions = []
        # def move(index, direction):
        #     code = pos[index]
        #     if code == 1:
        #         out = pos[:]


        # 上下相连
        if abs(bb- b) == 4:
            # 左右移横将
            

            # 左右移曹操

            # 左右移竖将

            # 左右移小兵
        
        # 左右相连
        elif bb-b ==1 and bb//4==b//4:

            # 第一步上下移动
            # look up ： 横将， 小兵， 竖将， 曹操
            if b> 3:
                if b>3 and 2 == pos[b-4] == pos[bb-4]:
                    newpos = pos[:]
                    newpos[b], newpos[bb], newpos[b-4], newpos[bb-4]= \
                        newpos[b-4], newpos[bb-4], newpos[b], newpos[bb] 
                    out.append(Board(prePawn = b, blankspace = [b-4,bb-4], pos = newpos))

                # 小兵可以走1 or 2格
                if b>3 and pos[b-4] ==1:
                    newpos = pos[:]
                    newpos[b], newpos[b-4] = newpos[b-4], newpos[b]
                    out.append(Board(prePawn = b, blankspace = [b-4,bb], pos = newpos))

                    # two blocks move
                    newpos = pos[:]
                    newpos[bb], newpos[b-4] = newpos[b-4], newpos[bb]
                    out.append(Board(prePawn = bb, blankspace = [b-4,b], pos = newpos))

                    # 对称格子
                    if pos[bb-4] == 1:
                        newpos = pos[:]
                        newpos[bb], newpos[bb-4] = newpos[bb-4], newpos[bb]
                        out.append(Board(prePawn = bb, blankspace = [bb-4,b], pos = newpos))

                        # two blocks move
                        newpos = pos[:]
                        newpos[b], newpos[bb-4] = newpos[bb-4], newpos[b]
                        out.append(Board(prePawn = b, blankspace = [bb-4,bb], pos = newpos))

                # shujiang
                for i, bi in enumerate(self.blankspace):
                    if bi>7 and 3== pos[bi-4]== pos[bi-8]:
                        newpos = pos[:]
                        newpos[bi], newpos[bi-8] = newpos[bi-8] , newpos[bi]
                        newblank = blankspace[:]
                        newblank[i] = bi-8
                        out.append(Board(prePawn = bi, blankspace = newblank, pos = newpos))
                # caocao
                if b>7 and 4 == pos[b-4]== pos[b-8] == pos[b-4 +1]== pos[b-8 +1]:
                    newpos = pos[:]
                    newpos[b], newpos[bb], newpos[b-8], newpos[bb-8]= \
                        newpos[b-8], newpos[bb-8], newpos[b], newpos[bb] 
                    out.append(Board(prePawn = b, blankspace = [b-8,bb-8], pos = newpos))


            # 左右移动





        # 空格不相连
        # 只能移动四周的兵
        # 存在死局么？
        else:
            for i,bi in enumerate(self.blankspace):
                swap = []
                # look around : up down left right
                if bi>3 and pos[bi-4] ==1:
                    swap.append(bi-4)
                if bi <16 and pos[bi+4] == 1:
                    swap.append(bi+4)
                if bi%4 > 0 :
                    swap.append(bi-1)
                if bi%4 < 3:
                    swap.append(bi+1)
                for sw in swap:
                    newpos = list(pos)
                    newpos[sw], newpos[bi] = newpos[bi], newpos[sw] 
                    newblank = list(self.blankspace)
                    newblank[i] = sw
                    out.append(Board(prePawn = bi, blankspace=newblank, pos = newpos))
        return out


    def printBoard(self):
        for i in range(len(self.pos)):
            print(self.pos[i], '')
            if i%4 == 3: print()







def ramGenerate():

    pass
    # return board


# encode int 
def enc(board):

    pass
    # code
    # return (code, father)

# decode 棋盘
def dec(code):

    pass
    # return board



def exits(code):

    # found before?
    # exits a mirror?



    return True





    # del exits board
    if not exits():
        append


    return boards, codes
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
        print("gg, sorry to inform you that there's no solution")
            


