import time 



class Board:
    '''保存华容道棋盘
    
    Variables:
        __upMovements {tuple} -- [description]
        ) {[type]} -- [description]
        __leftMovements {tuple} -- [description]
        ) {[type]} -- [description]
        __isoMovements {tuple} -- [description]
        ) {[type]} -- 
        三个movements静态变量： tuple 面4个int 依次表示
            pawn 相对空格的offset , code, offset, 
            tag: 1, 2, 3 : 水平，垂直， 折线移动： 定义不同的界限保证不穿墙

        heristic {list} -- 启发函数：曹操在不同层的h值
    '''
    __upMovements = (
        # 移曹操
        (-2, 4, 1, 1),
        (1, 4, -1, 1),
        # 移竖将 2+2*2 = 6 左右，一步； 上下，一步两步
        ( -1, 3, 1, 1),
        ( 1, 3, -1, 1),

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

        (-4, 1, 4, 2),
        (-4, 1, 8, 2),
        (8, 1, -4, 2),
        (8, 1, -8, 2)
    )

    # 左右相邻的空格
    __leftMovements = (
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
        # 移竖将       
        (-8,  3,   4, 2),
        (4,   3,   -4, 2),
        # 移横将       
        (-2,  2,   1, 1),
        (1,   2,   -1, 1),
        # 移小兵      
    )

    heristic = [41, 34, 6, 0]
    def __init__(self, pos, layer, blankspace = (0,0), prePawn =-1, pre = -1, father = -1 ):
        '''棋盘初始化一些参数
        
        封装对象尽可能少了解外部信息
        
        Arguments:
            pos {list} -- tuple可能更好一点，可以改写hash函数
                从左到右从上到下编码
                     空格 0
                     小兵 1
                     横将 2
                     竖将 3 
                     曹操 4
                         只编码左上角的，其余统一使用-1 

                 0  1  2  3 
                 4  5  6  7 
                 8  9  10 11 
                 12 13 14 15 
                 16 17 18 19 

            layer {int} -- 当前的遍历到的层数
        
        Keyword Arguments:
            blankspace {tuple} -- 现废弃 (default: {(0,0)})
            prePawn {number} -- 父节点生成该节点移动的节点，本节点不移动该节点能加快速度 (default: {-1})
            pre {number} -- 移动节点种类 0-4 (default: {-1})
            father {number} -- 父节点的指针 (default: {-1})
        
        Raises:
            Exception -- [description]
        '''
        self.pos = pos
        self.blankspace = [i for i,j in enumerate(pos) if j==0]
        self.prePawn = prePawn
        self.pre = pre
        self.layer = layer
        assert len(self.blankspace) == 2
        if not self.checkBoard():
            print('Generate bad board')
            self.printBoard()
            raise Exception
        # A*算法的启发函数
        self.A = self.layer + Board.heristic [self.pos.index(4)//4 ]
        self.father = father

    def gameover(self):
        if 4 ==self.pos[13]:
            return True
        else: return False

    def nextMove(self):
        '''从当前棋盘生成所有可能下一步棋盘
        
        整个程序最复杂的部分
        don't move the previous pawn
        # 两个空格相连时候兵可以走两个空格，可以拐弯，算一步
        
        Returns:
            list -- 生成的子棋盘
        '''

        b = self.blankspace[0]
        bb = self.blankspace[1]
        pos = self.pos 
        # 返回的棋盘list
        out = []

        # up down left right; 
        # it's about pawn not move blank space!
        # return new pos 
        def move(index, offset):
            '''把index指向的棋子向offset方向移动
            
            因为是一维数组编码，当时考虑的不是很充足，出现很多bug，最主要的是棋子"穿墙过"的情况
            
            Arguments:
                index {int} -- 当前棋子pos 的index
                offset {int} -- 位移
            
            Returns:
                list -- 棋盘的pos
            '''
            # code 棋子的种类代码： 0 空格， 。。
            code = pos[index]
            out = pos[:]

            # 移动曹操
            if code == 4:
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
            elif code == 3:
                # left - right:  equal to swap
                # up -down 2 blocks : equal to swap
                if offset in [-1, 1, -8, 8]:
                    out[index], out[index+4], out[index+offset], out[index+4+offset] =\
                    out[index+offset], out[index+4+offset], out[index], out[index+4]
                # insert sort
                else:
                    #  up
                    if offset == -4:
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
            for i,m in enumerate(Board.__upMovements):
                if -1< b+m[0]<20 and pos[b+m[0]] == m[1]:
                    flag = True
                    # 水平移动最复杂
                    if m[3] ==1:
                        # 小兵 移动前后在同一线上
                        if m[1] ==1 and (b+m[0])//4 != (b+m[0]+m[2])//4: flag = False
                        # 横将和曹操 移动之后不能半身截断
                        if m[1] in [2,4] and (b+m[0]+m[2])%4 == 3: flag = False
                        # 竖将 和空格同一水平线
                        if m[1] ==3 and b//4!= (b+m[0])//4: flag = False 
                    # 折线移动
                    elif m[3] == 3:
                        if m[0] in [-1, 1] and (b+m[0])//4 != b//4: flag = False
                        if m[0] in [3,5] and (b+m[0]) // 4 != bb//4 : flag = False
                    # 垂直运动不限制
                    if flag: 
                        out.append(Board(move(b+m[0], m[2]), prePawn = b+m[0], pre = pos[b+m[0]], layer = self.layer+1, father = self))
       
        # 左右相连
        elif abs(bb-b) ==1 and bb//4==b//4:
            for i,m in enumerate(Board.__leftMovements):
                if -1< b+m[0]<20 and pos[b+m[0]] == m[1]:
                    # 水平移动保证在同一层   
                    # 空格和格子在同一水平线
                    if m[3] == 1 and  b//4 ==(b+m[0])//4  or m[3] !=1 :
                        out.append(Board(move(b+m[0], m[2]), prePawn = b+m[0], pre = pos[b+m[0]], layer = self.layer+1, father = self))

        # # 空格不相连: 移动横将，竖将，兵
        else:
            # 查看四周的小兵
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
                    out.append(Board(pos = newpos, prePawn = sw, pre = pos[sw], layer = self.layer+1, father = self))

                # 横将竖将
                for m in Board.__isoMovements:
                    # 不能随便复制粘贴哇。。
                    if -1< bi+m[0]<20 and pos[bi+m[0]] == m[1]:
                        # 空格和横将, 只有横将水平移动 同一行
                        if m[3] == 1 and (bi)//4 != (bi+m[0]) //4 :
                            continue
                        out.append(Board(move(bi+m[0], m[2]), prePawn = bi+m[0], pre = pos[bi+m[0]], layer = self.layer+1, father = self))
               
        return out


    def printBoard(self):
        for i in range(len(self.pos)):
            if self.pos[i] == -1:
                print(' ', '', end= '')
            else:
                print(self.pos[i], '' , end= '')
            if i%4 == 3: print()

        # print('pre %d === prePawn %d==========================' %(self.prePawn, self.pre))


    # 确认当前棋盘是否有问题， 主要debug 和 初试棋盘确认用
    def checkBoard(self):
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


    # 生成镜像的棋盘的pos列表
    def mirrorPos(self):
        mir = []
        for i in range(0, 17, 4):
            mir.extend(self.pos[i: i+4][::-1])
        # !! 非对称编码 4, 1 需要和左边的-1 交换
        for i, m in enumerate(mir):
            if m in [2, 4]:
                mir[i], mir[i-1] = mir[i-1], mir[i]
        return tuple(mir)


# 一些经典棋盘； 输入i 可以选择具体棋盘  ； 依次是
# 横刀立马 81   水泄不通 79   一路进军 58   峰回路转 138   过五关 34       
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
      
    return Board(li[i] , layer = 0)


# 递归打印，前面版本的BFS搜索使用，heuristic搜索的时候已经废弃
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
def solution(iniBoard , mirror = True, printed = False, heristic = True):
    '''求解棋盘函数
    
    可以选择是否使用  ： 镜像查重， 启发搜索
    
    Arguments:
        iniBoard {Board} -- 棋盘初试状态
    
    Keyword Arguments:
        mirror {bool} -- 是否使用镜像 (default: {True})
        printed {bool} -- 是否打印棋盘过程 (default: {False})
        heristic {bool} -- 是否使用启发搜索 (default: {True})
    
    Returns:
        tuple -- 运行的时间，搜索的节点数等
    '''
    # if iniBoard.gameover: !!!
    if iniBoard.gameover():
        print('already a solution, no need to move ')
        return (0,0)
    if heristic:
        # Python标准库，可以动态顺序插入， 时间复杂度log(N)
        import bisect
        iwait = [iniBoard.A]
        openli = []
        openli.append(iniBoard)
        closeli = []

        visited = set(tuple(iniBoard.pos))
        if mirror: visited.add(iniBoard.mirrorPos())
        st = time.time ()

        while len(openli) > 0:
            curBoard = openli.pop(0)
            iwait.pop(0)
            closeli.append(curBoard)

            sonBoards = curBoard.nextMove()
            for sBoard in sonBoards:
                tp = tuple(sBoard.pos)
                if tp not in visited :
                    if mirror:
                        mirr = sBoard.mirrorPos()
                        if mirr in visited: continue
                        else: visited.add(mirr)
                    visited.add(tp)
                    # 按照A值插入列表, 
                    insert = bisect.bisect(iwait, sBoard.A)
                    openli.insert(insert, sBoard)
                    iwait.insert(insert, sBoard.A)

                    if sBoard.gameover():
                        # print('----%d' %sBoard.A)
                        end = time.time ()
                        # 打印运行结果
                        if printed:
                            def recur(board):
                                if board.father == -1:
                                    print('heristic search step %d' %board.layer)
                                    board.printBoard()
                                else:
                                    recur(board.father)
                                    print('heristic search step %d' %board.layer)
                                    board.printBoard()
                            recur(sBoard)
                            print('heristic machine has tried %d moves' % (len(openli) + len(closeli) +1))
                        # print(cover)
                        return end -st, len(openli)+len(closeli)

        print("gg, sorry to inform you that there's no solution")
        print('machine has tried %d moves' % cur)
        end = time.time ()
        return(end-st, cur+1) 

    # BFS 搜索

    #存放 like (int, int father_point)
    queue = []
    queue.append((iniBoard, -1))
    cur = 0

    visited = set(tuple(iniBoard.pos))
    if mirror: visited.add(iniBoard.mirrorPos())
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
                    # print('----%d' %sBoard.A)
                    end = time.time ()
                    # 打印运行结果
                    if printed:
                        previous = queue[-1]
                        count = printPre(previous, queue, )
                        print('machine has tried %d moves' % (cur+1))
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
        # 把printed = True 就能够打印棋盘结果了
        print('heuristic mirror search cost %f seconds and %dmoves' %solution(iniBoard , mirror = True, printed = False, heristic = True))
        print('BFS mirror search cost %f seconds and %dmoves' %solution(iniBoard , mirror = True, printed = False, heristic = False))
        print('heuristic search withous mirror detection cost %f seconds and %dmoves' %solution(iniBoard , mirror = False, printed = False, heristic = True))
        print('BFS search withous mirror detection cost %f seconds and %dmoves' %solution(iniBoard , mirror = False, printed = False, heristic = False))
