

# from collections import Counter 
# cover = Counter()

class Board:
    
    '''保存华容道棋盘类
    '''
    # blankspace 暂时没有用！！ 这个参数暂时删除
    # prePawn 暂时删除


    # 静态变量：
    '''
    pawn 相对空格的offset , code, offset, tag: 1, 2, 3 : 水平，垂直， 折线移动： 定义不同的界限保证不穿墙
    水平 & 折线这两种情况有可能“穿墙” 而过！！ 
        水平： 移动不能到下一层
            index //4 和 (index+offset) // 4 要保证相等
        折线 -- 小兵： 
            只需要考虑垂直相邻的两个空格的折线
                上两个 ： pawn 要b//4 同一层
                下两个 ： 要和 bb 同一层

    最好还是定义成为静态的

    '''
    __upMovements = (
        # pawn相对空格的offset , code, offset, tag: 1, 2, 3 : 水平，垂直， 折线移动： 定义不同的界限保证不穿墙
        # 移曹操
        (-2, 4, 1, 1),
        (1, 4, -1, 1),
        # 移竖将 2+2*2 = 6 左右，一步； 上下，一步两步
        ( -1, 3, 1, 1),
        ( 1, 3, -1, 1),

        # ( -4, 3, 4, 2), # 没有执行过
        # ( -4, 3, 8, 2), # 没有执行过
        (-8, 3, 4, 2),
        (-8, 3, 8, 2),

        ( 8, 3, -4, 2),
        ( 8, 3, -8, 2),
        # 移横将 4 左右四个角
        (-2 , 2, 1, 1),
        ( 1, 2, -1, 1),
        (2, 2, 1, 1),
        ( 5, 2, -1, 1),
        # 移小兵 4*2+ 2*2 = 12 左右，一步两步 (两个格子就是折线)； 上下， 一部两步
        (-1, 1, 1, 1),
        (3, 1, 1, 1),
        (-1, 1, 5, 3),
        (3, 1, -3, 3),

        (1, 1, -1, 1),
        (5, 1, -1, 1),
        (1, 1, 3, 3),
        (5, 1, -5, 3), # 没有执行过

        # (-1, 1, 4),
        # (-1, 1, 8),
        (-4, 1, 4, 2),
        (-4, 1, 8, 2),
        (8, 1, -4, 2),
        (8, 1, -8, 2)
    )

    # 左右相邻的空格
    __leftMovements = (
        # pawn相对空格的offset , code, offset , tag: 1, 2, 3 : 水平，垂直， 折线移动： 定义不同的界限保证不穿墙    
        # 移曹操       2
        # (-4  ,4,   4,),
        (-8, 4, 4  ,2),
        (4   ,4,   -4, 2),
        # 移竖将       4
        (-8  ,3,   4, 2),
        (-7  ,3,   4, 2),
        (4   ,3,   -4, 2),
        (5   ,3,   -4, 2),
        # 移横将       左右2*2 上下2 = 6
        (-2 , 2,   1, 1),
        (-2  ,2,   2, 1),
        (2   ,2,   -1, 1),
        (2   ,2,   -2, 1),
        (-4  ,2,   4, 2),
        (4   ,2,   -4, 2),
        # 移小兵       左右2*2 上下4*2 = 12
        (-1  ,1   ,1, 1),
        (-1  ,1   ,2, 1),
        (2   ,1   ,-1, 1),
        (2   ,1   ,-2, 1),
             
        (-4  ,1   ,4, 2),
        (-4  ,1   ,5, 3),
        (-3  ,1   ,4, 2),
        (-3  ,1   ,3, 3),

        (4   ,1   ,-4, 2),
        (4   ,1   ,-3, 3),
        (5   ,1   ,-4, 2),
        (5   ,1   ,-5, 3),
    )

    # 不相邻的格子
    # 兼容move 函数，，， thank GOD..
    __isoMovements =(
        # pawn相对空格的offset , code, offset  , tag: 1, 2, 3 : 水平，垂直， 折线移动： 定义不同的界限保证不穿墙   
        # 移竖将       
        (-8,  3,   4, 2),
        (4,   3,   -4, 2),
        # 移横将       
        (-2,  2,   1, 1),
        (1,   2,   -1, 1),
        # 移小兵      

    )

    def __init__(self, pos, blankspace = (0,0), prePawn =-1, pre = -1 ):
        '''[summary]
        
        [description]
        封装对象不需要知道额外的信息
        Arguments:
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
        self.pos = pos
        self.blankspace = [i for i,j in enumerate(pos) if j==0]
        self.prePawn = prePawn
        self.pre = pre
        assert len(self.blankspace) == 2
        if not self.checkBoard():
            print('Generate bad board')
            self.printBoard()
            raise Exception
        # assert self.checkBoard(), 'Generate bad board'
        # self.prePawn = prePawn

    def gameover(self):
        # if 4 in self.pos[8:]:
        #     print('move one layer already')
        if 4 ==self.pos[13]:
        # ==self.pos[14]==self.pos[17]==self.pos[18]:
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

        # up down left right; 
        # it's about pawn not move blank space!
        # return new pos 
        def move(index, offset):
            code = pos[index]
            out = pos[:]
            # 曹操， ;;虽然有两个格子可以不用移动，但是我懒~
            # your karma has come
            if code == 4:
                # out[index], out[index+1], out[index+4], out[index+5],\
                # out[index+offset], out[index+1+offset], out[index+4+offset], out[index+5+offset] =\
                # out[index+offset], out[index+1+offset], out[index+4+offset], out[index+5+offset],\
                # out[index], out[index+1], out[index+4], out[index+5]

                if offset == -1:
                    assert out[index-1] == out [index+3] == 0
                elif offset == 1:
                    assert out[index+2] ==  out[index+6] == 0
                elif offset == -4:
                    assert out[index-4] == out[index-3] == 0
                elif offset == 4:
                    assert out[index+8] == out[index + 9] == 0

                out[index+offset], out[index+1+offset], out[index+4+offset], out[index+5+offset] =\
                out[index], out[index+1], out[index+4], out[index+5]
                if offset == -1:
                    out[index+1] = out[index+5] = 0
                elif offset == 1:
                    out[index] =  out[index+4] = 0
                elif offset == -4:
                    out[index+4] = out[index+5] = 0
                elif offset == 4:
                    out[index] = out[index + 1] = 0

                

            # 竖将
            # elif code == 1:
            elif code == 3:
                # 假如往下移动一格是有问题的！这样子重复赋值操作并不能达到方块下移一格，空格向上移动2格！
                # 移动格子不是交换位置！
                # print(out[index], out[index +4], out[index+offset], out[index +4+offset])
                # out[index], out[index+4], out[index+offset], out[index+4+offset] =\
                # out[index+offset], out[index+4+offset], out[index], out[index+4]

                # left - right:  equal to swap
                # up -down 2 blocks : equal to swap
                if offset in [-1, 1, -8, 8]:
                    out[index], out[index+4], out[index+offset], out[index+4+offset] =\
                    out[index+offset], out[index+4+offset], out[index], out[index+4]
                # insert sort
                else:
                    #  up
                    if offset == -4:
                        # tmp is int 0: blankspace
                        assert out[index-4] == 0
                        out[index-4], out[index] = out[index], out[index+4]
                        out[index+4] = 0
                    elif offset == 4:
                        assert out[index+8] == 0
                        out[index+4] , out[index+8] = out[index], out[index+4]
                        out[index] = 0
                    else:
                        assert 0==3
            # 横将
            elif code == 2:
                if offset in [-2, 2, -4, 4]:
                    assert out[index+offset]== out[index +1+offset] == 0
                    out[index+offset], out[index +1+offset], out[index], out[index +1] =\
                    out[index], out[index +1], out[index+offset], out[index +1+offset]
                elif offset == -1:
                    assert out[index-1] == 0
                    out[index+offset], out[index +1+offset] = \
                    out[index], out[index +1]
                    out[index+1] = 0
                elif offset == 1:
                    assert out[index+2] == 0
                    out[index+offset], out[index +1+offset] = \
                    out[index], out[index +1]
                    out[index] = 0

            # 小兵
            else:
                assert out[index+offset] == 0, '小兵移动目标不是空格： index = %d, offset = %d' %(index, offset)
                out[index + offset], out[index] = out[index], out[index + offset]
            
            return out
                
        # 上下相连
        if abs(bb- b) == 4:
            # 之后在把全局变量放在外面，节省空间
            # 必须测试一下！！ 头都晕了很容易出错
            # global upMovements
            # global cover
            for i,m in enumerate(Board.__upMovements):
                if -1< b+m[0]<20 and pos[b+m[0]] == m[1]:
                    flag = True
                    # 水平移动最复杂
                    if m[3] ==1:
                        # 小兵 移动前后在同一线上
                        if m[1] ==1 and (b+m[0])//4 != (b+m[0]+m[2])//4: flag = False
                        # 横将和曹操 移动之后不能半身截断
                        # if m[1] in [2,4] and (b+m[0]+m[2])%4 != 3: flag = False
                        if m[1] in [2,4] and (b+m[0]+m[2])%4 == 3: flag = False
                        # 竖将 和空格同一水平线
                        if m[1] ==3 and b//4!= (b+m[0])//4: flag = False 
                    # 折线移动
                    elif m[3] == 3:
                        if m[0] in [-1, 1] and (b+m[0])//4 != b//4: flag = False
                        # if m[0] in [3, 5] and (bb+m[0])//4 != bb//4: flag = False
                        if m[0] in [3,5] and (b+m[0]) // 4 != bb//4 : flag = False
                    # 垂直运动不限制
                    if flag: 
                        out.append(Board(move(b+m[0], m[2]), prePawn = b+m[0], pre = pos[b+m[0]]))
                        # cover[i] +=1
                    # if m[0] == -4 and m[2] == 8: print('-=======================================-==--=-=-=')
       
        # 左右相连
        elif abs(bb-b) ==1 and bb//4==b//4:
            # global leftMovements
            for i,m in enumerate(Board.__leftMovements):
                if -1< b+m[0]<20 and pos[b+m[0]] == m[1]:
                    # 水平移动保证在同一层   
                    # 空格和格子在同一水平线
                    if m[3] == 1 and  b//4 ==(b+m[0])//4  or m[3] !=1 :
                        out.append(Board(move(b+m[0], m[2]), prePawn = b+m[0], pre = pos[b+m[0]]))
                        # cover[i+24] +=1

  

        # # 空格不相连: 移动横将，竖将，兵
        else:
            for i,bi in enumerate(self.blankspace):
                swap = []
                # look around : up down left right
                if bi>3 and pos[bi-4] ==1:
                    swap.append(bi-4)
                if bi <16 and pos[bi+4] == 1:
                    swap.append(bi+4)
                if bi%4 > 0  and pos[bi-1] == 1:
                    swap.append(bi-1)
                if bi%4 < 3 and pos[bi+1] == 1:
                    swap.append(bi+1)
                for sw in swap:
                    newpos = list(pos)
                    newpos[sw], newpos[bi] = newpos[bi], newpos[sw] 
                    out.append(Board(pos = newpos, prePawn = sw, pre = pos[sw]))

                # 横将竖将
                # global isoMovements
                for m in Board.__isoMovements:
                    # 不能随便复制粘贴哇。。
                    # if -1< b+m[0]<20 and pos[b+m[0]] == m[1]:
                    #     out.append(Board(move(b+m[0], m[2])))
                    if -1< bi+m[0]<20 and pos[bi+m[0]] == m[1]:
                        # # 水平移动保证在同一层   
                        # # if m[3] == 1 and (b+m[0])//4 == (b+m[0]+m[2])//4 or m[3] !=1:
                        # # again ? same mistake>?? 不要复制粘贴。。
                        # if (m[3] == 1 and (bi+m[0])//4 == (bi+m[0]+m[2])//4) or m[3] !=1:
                        #     self.printBoard() 

                        # 空格和横将, 只有横将水平移动 同一行
                        if m[3] == 1 and (bi)//4 != (bi+m[0]) //4 :
                            continue
                        out.append(Board(move(bi+m[0], m[2]), prePawn = bi+m[0], pre = pos[bi+m[0]]))
               
        return out


    def printBoard(self):
        for i in range(len(self.pos)):
            if self.pos[i] == -1:
                print(' ', '', end= '')
            else:
                print(self.pos[i], '' , end= '')
            if i%4 == 3: print()

        print('pre %d === prePawn %d==========================' %(self.prePawn, self.pre))

    def checkBoard(self):
        # dic = {}
        # 全部都是横将
        dic = {i:0 for i in range(-1,5)}
        if len(self.pos) != 20:
            return False
        pos = self.pos
        for i,p in enumerate(self.pos):
            # print(self.pos)
            if p==4:
                # 不能跨墙啊！！ or i%4 == 3:
                if not -1== pos[i+1] ==pos[i+4] ==pos[i+5]\
                or i%4 == 3:
                    return False
            elif p== 3:
                if -1!= pos[i+4]:
                    return False
            elif p==2 :
                if -1 != pos[i+1] \
                or i%4 == 3: 
                    return False

            dic[p]+=1
        if dic[4]!= 1 or dic[3]+dic[2] != 5 or dic[1] != 4:
            # print(dic)
            return False
        return True

    def mirrorPos(self):
        mir = []
        for i in range(0, 17, 4):
            mir.extend(self.pos[i: i+4][::-1])
        # !! 非对称编码 4, 1 需要和左边的-1 交换
        for i, m in enumerate(mir):
            if m in [2, 4]:
                mir[i], mir[i-1] = mir[i-1], mir[i]
        # assert Board(mir).checkBoard
        return tuple(mir)
def generateBoard(i=0):

    li= [ [
    # 横刀立马 81 check
        3, 4, -1,  3, 
        -1, -1, -1,-1, 
        3, 2, -1, 3, 
        -1 , 1, 1, -1, 
        1, 0, 0, 1, 
    ]

    # 水泄不通 79 check
    , [3, 4, -1, 1,
        -1, -1, -1, 1,
        2, -1, 2,-1,
        2, -1, 2, -1,
        1, 0, 0, 1]
  
    # 一路进军 58 check
    , [3, 4, -1, 1,
    -1, -1, -1, 1,
    3, 3, 3, 1,
    -1, -1, -1, 1,
    0, 2, -1, 0]
 
    # 峰回路转 138  check
    , [1,1,1,3,
        4,-1,3,-1,
        -1,-1,-1,3,
        0,2,-1,-1,
        0,1,2,-1]
    # 过五关 34 check
    ,[1, 4, -1, 1,
        1, -1, -1, 1,
        2, -1, 2, -1,
        2, -1, 2, -1,
        0, 2, -1, 0]
    ]
    # 横刀立马 81   水泄不通 79   一路进军 58   峰回路转 138   过五关 34   
    return Board(li[i] )

def printPre(previous, queue, ):
    '''递归回溯到第一步， 打印走棋过程
    Arguments:
        previous {tuple} -- Board, father's index
        queue {list} -- contains the tuple
    
    Returns:
        int -- current step's count
    '''
    if previous[1] == -1:
        # 初始状态， 还未移动
        count = 0
        print('this is the No.%d step' %count)
        previous[0].printBoard()
        return count
    else:
        count = printPre(queue[previous[1]], queue, ) +1
        print('this is the No.%d step' %count)
        previous[0].printBoard()
        return count

# mirror: bool; printed :bool; 
# return time, search moves, 
def solution(iniBoard , mirror = True, printed = False):

    # like (int, int father_point)
    queue = []
    # if iniBoard.gameover: !!!
    if iniBoard.gameover():
        print('already a solution, no need to move ')
        raise SystemExit
    queue.append((iniBoard, -1))
    cur = 0

    visited = set(tuple(iniBoard.pos))
    if mirror: visited.add(iniBoard.mirrorPos())
    # print(iniBoard.pos, iniBoard.mirrorPos())

    import time 
    st = time.time ()

    # BFS search
    while cur<len(queue):
        curBoard = queue[cur][0]
        # curBoard.printBoard()
        sonBoards = curBoard.nextMove()
        for sBoard in sonBoards:
            tp = tuple(sBoard.pos)
            if tp not in visited :
                if mirror:
                    mirr = sBoard.mirrorPos()
                    if mirr in visited: continue
                    else: visited.add(mirr)
                visited.add(tp)
                queue.append((sBoard, cur))
                if sBoard.gameover():
                    end = time.time ()
                    # 打印运行结果
                    if printed:
                        previous = queue[-1]
                        count = printPre(previous, queue, )
                        print('machine has tried %d moves' % (cur+1))
                    # print(cover)
                    return end -st, cur+1
        cur+=1

    if cur == len(queue):
        print("gg, sorry to inform you that there's no solution")
        print('machine has tried %d moves' % cur)
        end = time.time ()
        return(end-st, cur+1)

if __name__ == '__main__':
    for i in range(5):
        iniBoard = generateBoard(i)
        # iniBoard = generateBoard(0)
        print('mirror search cost %f seconds and %dmoves' %solution(iniBoard, True,))
        print('search cost %f seconds and %dmoves' %solution(iniBoard, False))
