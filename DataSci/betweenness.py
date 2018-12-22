#!/usr/bin/python
# -*- coding:utf-8 -*-
import itertools
import math
import sys


def get_cur_info():
    print
    sys._getframe().f_code.co_filename  # 当前文件名
    print
    sys._getframe(0).f_code.co_name  # 当前函数
    print
    sys._getframe(1).f_code.co_name  # 调用该函数的函数的名字，如果没有被调用，则返回modul
    print
    sys._getframe().f_lineno  # 当前行号


'''
map 是一个Python里面的原有函数，这里图省事直接占用，懒得改了
'''

# top triangle valid 对称
mapT1 = [
    [-1, 1, 0, 0, 0, 1, 1],
    [1, -1, 1, 0, 0, 1, 0],
    [0, 1, -1, 0, 0, 0, 1],
    [0, 0, 0, -1, 1, 0, 1],
    [0, 0, 0, 1, -1, 1, 0],
    [1, 1, 0, 0, 1, -1, 1],
    [1, 0, 1, 1, 0, 1, -1]
]
mapT2 = [
    [-1, 1, 1, 0, 0, 1, 1], [1, -1, 1, 0, 1, 1, 0],
    [1, 1, -1, 0, 0, 0, 1], [0, 0, 0, -1, 1, 1, 1],
    [0, 1, 0, 1, -1, 1, 1], [1, 1, 0, 1, 1, -1, 1],
    [1, 0, 1, 1, 1, 1, -1]
]


# 复制一个二维数组，深复制
def copyMap(map):
    row = len(map)
    map1 = [[] for i in range(row)]
    for i in range(len(map)):
        for col in range(len(map[i])):
            map1[i].append(map[i][col])
    return map1


# 计算a 到k所有所有点的最短路径，并且返回边介值矩阵
def BFS(mapT, a, k):
    row = len(mapT)
    # map 存储 边介质数，矩阵上面的数值代表介数值，初始化为0
    map = [[0 for i in range(row)] for j in range(row)]
    # shortP 每个节点的最短路径数，从a 到 k 经过的。 初始化为0
    shortP = [0 for i in range(row)]
    # 当前搜索的层，根据layer层节点-->寻找下一层的节点
    layer = 0
    # reach[]存贮已经到达的节点号
    reach = [a]
    # path{} ，BFS搜索中每层 layer 的节点
    path = {layer: [a]}

    while (layer == len(path) - 1):
        # 终点k 在reach 终止BFS
        if k in reach:
            break
        # BFS ，一直到找到 k 终点
        currentLayerLen = len(path[layer])
        # 当前layer搜索
        for i in range(currentLayerLen):
            index = path[layer][i]
            # 寻找 上一层队列里面index节点--> 的下一层 节点（不在reach 里面的节点）
            for col in range(row)
                # 我设计错误，reach 和 计算shortP 冲突
                # col已经搜索到了，把col的最短路径书相加 ---
                # layer == len( path)-2 保证不会越界
                # if layer == len( path)-2 and col in path[layer+1] and mapT[index][col] == 1 : 
                # shortP[col] +=shortP[index]

                # col第一次找到
                if mapT[index][col] == 1 and col not in reach:
                    reach.append(col)
                    # 更新shortP的值
                    if layer == 0:
                        shortP[col] = 1
                    else:
                        shortP[col] += shortP[index]
                    # 新建一layer
                    if layer + 1 not in path.keys():
                        path[layer + 1] = [col]

                    else:
                        if col not in path[layer + 1]:
                            path[layer + 1].append(col)
                            # 在下一层被之前index找到的下一层节点，累加最短路径
                if mapT[index][col] == 1 and layer == len(path) - 2 and col in path[layer + 1]:
                    shortP[col] += shortP[index]
        layer += 1

    # 最后一层，不光光是k的话，你得忽略！！
    layer = len(path) - 1
    # print "layer",layer
    if k not in path[layer]:
        print
        "没有最短路径"
    # 清除最后一层的shortP，只留下终点 k
    else:
        for i in path[layer]:
            if not i == k:
                shortP[i] = 0
        path[layer] = [k]

    # 每一层可能会有一些无关的，不能到达 终点k 的一些值，需要忽略！！
    ##好像并不影响……

    # 以下是溯回程序
    # 最初0 设置为1 ，并不影响
    shortP[a] = 1

    betw = [0 for i in range(row)]
    betw[k] = 1.0

    while layer > 0:
        for curLayer in path[layer]:
            linked = []
            pathNum = 0.0
            for preLayer in path[layer - 1]:
                if mapT[curLayer][preLayer] == 1:
                    linked.append(preLayer)
                    pathNum += shortP[preLayer]
            for l in linked:
                # import pdb
                # pdb.set_trace()
                # if pathNum == 0 : 
                betw[l] += shortP[l] / pathNum * betw[curLayer]
                map[curLayer][l] = betw[l]
                map[l][curLayer] = betw[l]
        layer -= 1

    return map


# 把两个二维数组相加到map1
def matrixAdd(map1, map2):
    lenth = len(map1)
    for i in range(lenth):
        for j in range(lenth):
            map1[i][j] += map2[i][j]


# 保留两位小数输出二维数组
def prettyOutput(map1):
    lenth = len(map1)
    for i in range(lenth):
        for j in range(lenth):
            print
            str("%.2f" % map1[i][j]),
        print


# 利用特制的BFS， 计算所有的边betweenness，和点betweenness
# betwMap[[]] 是边介值矩阵
def betweeness(mapT):
    x = len(mapT)
    betwMap = [[0 for i in range(x)] for j in range(x)]
    for i in range(x):
        for j in range(x):
            if not i == j:
                matrixAdd(betwMap, BFS(mapT, i, j))
    return betwMap


prettyOutput(betweeness(mapT2))


# BFS(mapT2,0,3)
# BFS(mapT2,0,4)
# BFS(mapT2,0,1)
# BFS(mapT2,0,3)
# BFS(mapT2,0,3
