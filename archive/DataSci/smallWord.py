#!/usr/bin/python
# -*- coding:utf-8 -*-
# 小世界现象的验证，同时用面向对象来封装之前的betweenness  写的程序。
import random


class rate:
    def __init__(self, map1, num):
        self.map = map1
        self.layers = num
        self.rows = len(map1)

    def isSix(self, start):

        layer = 0
        reach = [start]
        # path{} ，存储每个节点对应最短路径个数
        path = {layer: [start]}
        # t条件刚好弄反了，写代码长了，反而找不出来？这种高内聚 ？？该怎么写？
        while len(reach) != self.rows and layer != self.layers:
            # 搜索完成，不能扩张新的节点
            if layer not in path.keys():
                break
            # BFS 遍历layer 这一层
            currentLayerLen = len(path[layer])
            for i in range(currentLayerLen):
                index = path[layer][i]

                for col in range(self.rows):
                    # !!
                    if self.map[index][col] == 1 and col not in reach:
                        reach.append(col)
                        if layer + 1 not in path.keys():
                            path[layer + 1] = [col]
                        else:
                            path[layer + 1].append(col)
            layer += 1
        print(len(reach))
        # print "num",start,"---reach- length--",len(reach),"---------reach is ----------",reach
        # print "path is ---",path
        if (len(reach) == self.rows):
            return 1
        else:
            return 0

    def rate(self):
        issix = 0
        for i in range(self.rows):
            if self.isSix(i):
                issix += 1
        print(issix)
        return (issix + 0.0) / self.rows


def randomMatrix(num):
    matrix = []
    for i in range(num):
        row = []
        for j in range(num):
            if random.random() > 0.99:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    return matrix


def change(map):
    row = len(map)
    for i in range(0, row):
        for j in range(0, i):
            map[i][j] = map[j][i]
    for i in range(0, row):
        map[i][i] = -1
    return map


mapT2 = [
    [-1, 1, 1, 0, 0, 1, 1], [1, -1, 1, 0, 1, 1, 0],
    [1, 1, -1, 0, 0, 0, 1], [0, 0, 0, -1, 1, 1, 1],
    [0, 1, 0, 1, -1, 1, 1], [1, 1, 0, 1, 1, -1, 1],
    [1, 0, 1, 1, 1, 1, -1]
]


def test(num, cut):
    matr = change(randomMatrix(num))
    # print "the random map is ------------------------------------------------------------"
    # for i in range (num):
    #     print matr[i]
    six = rate(matr, cut)
    print(six.rate())


# test(1000,6)
# test(1000,4)
test(1000, 3)
# test (500,4)
# test(100,3)
# test(100,2)

# five = rate(mapT2,2)
# print five.rate()
