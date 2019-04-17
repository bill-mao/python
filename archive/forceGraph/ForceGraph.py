import random
import math
import sys
import pygame
import time
import threading
from pygame.locals import *  #导入一些常用的函数和常量


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.force_x = 0
        self.force_y = 0

    def getNeighborLength (self):
        return len(self.neighbors)

    def setNeighbor(self, neighbors):
        self.neighbors = neighbors

    def addNeighbor(self, i):
        self.neighbors.append(i)



class ForceGraph :
    def __init__(self, num, nodes):
        self.nodes = nodes
        self.N = self.nodesNum = num
        self.L = self.nodesNum * 2  # spring rest length 弹簧的初始长度
        self.ratio = 6  # 由用户设置，根据产生的图的形状来调整参数, 越大斥力越大# 改进算法
        self.K_s = 111  # spring constant
        self.K_r = self.K_s * self.ratio
        self.delta_t = 3  # time step， 值可以动态设置，刚开始大一点- 运行速度快；后面慢一点，保证能够收敛
        self.MAX_DISPLACEMENT_SQUARED = 20  # 缓冲，防止一下子运动太多的距离
        # 改进算法
        self.temperature = self.nodesNum / 100 +50  # 让delta_t能够动态改变大小, 随着迭代次数增加，不断减少
        self.iterationCount = 0  # 随着迭代的次数增加而下降  temperature = temperature / 1.2
        self.farDistance = 200  # 当超过这个值的时候，斥力就不计算了，优化运行速度
        self.randomForce = 2.5
        # 迭代终止条件
        self.MAX_ITERATION = 1000
        # self.MIN_ENERGY = math.ceil(((1000000) * nodesNum) /100)
        self.MIN_ENERGY = math.ceil(((100000) * self.nodesNum) / 100)
        # self.MIN_ENERGY = (1e6) * nodesNum
        self.energy = 0


        # 画图到里面去了
        self.offset = math.ceil(self.nodesNum) + 111
        self.height = self.nodesNum * 4 + 222
        self.width = self.nodesNum * 4 + 222

        #开始
        print("节点数， 花费时间 "+ str(self.N) +"  "+ str(self.start_ite()))

        # self.drawPic()

    def iteratePosition(self):
        self.iterationCount += 1
        self.energy = 0
        # initialize net forces
        for i in range(self.N):
            self.nodes[i].force_x = 0
            self.nodes[i].force_y = 0

        # repulsion between all pairs
        for i1 in range(self.N):
            node1 = self.nodes[i1]
            for i2 in range(i1 + 1, self.N):
                node2 = self.nodes[i2]
                dx = node2.x - node1.x
                dy = node2.y - node1.y
                if dx > self.farDistance or dy > self.farDistance:
                    continue
                if dx != 0 or dy != 0:
                    distanceSquared = dx * dx + dy * dy
                    distance = math.sqrt(distanceSquared)
                    force = K_r / distanceSquared * 1.3
                    self.energy += force
                    fx = force * dx / distance
                    fy = force * dy / distance
                    node1.force_x = node1.force_x - fx
                    node1.force_y = node1.force_y - fy
                    node2.force_x = node2.force_x + fx
                    node2.force_y = node2.force_y + fy
                # ***产生一个随机的small的力，保证在两个重合节点有相同的邻居时候能够运动
                else:
                    fx = random.random() * self.randomForce
                    fy = random.random() * self.randomForce
                    node1.force_x = node1.force_x - fx
                    node1.force_y = node1.force_y - fy
                    node2.force_x = node2.force_x + fx
                    node2.force_y = node2.force_y + fy

        # spring force between adjacent pairs
        for i1 in range(self.N):
            node1 = self.nodes[i1]
            for j in range(0, node1.getNeighborLength()):
                i2 = node1.neighbors[j]
                node2 = self.nodes[i2]
                # 防止重复
                if i1 < i2:
                    dx = node2.x - node1.x
                    dy = node2.y - node1.y
                    if dx != 0 or dy != 0:
                        distance = math.sqrt(dx * dx + dy * dy)
                        force = K_s * (distance - self.L)  # 减去弹簧长度， 胡克定律
                        self.energy += force
                        fx = force * dx / distance
                        fy = force * dy / distance
                        node1.force_x = node1.force_x + fx
                        node1.force_y = node1.force_y + fy
                        node2.force_x = node2.force_x - fx
                        node2.force_y = node2.force_y - fy
        # update positions

        for i in range(self.N):
            node = self.nodes[i]
            # 动态改变delta_t，刚开始快，后来慢，保证收敛
            dx = self.temperature * self.delta_t * node.force_x
            dy = self.temperature * self.delta_t * node.force_y
            # 减少开方运算，提高速度
            displacementSquared = dx * dx + dy * dy
            if displacementSquared > self.MAX_DISPLACEMENT_SQUARED:
                s = math.sqrt(self.MAX_DISPLACEMENT_SQUARED / displacementSquared)
                dx = dx * s
                dy = dy * s
            node.x = node.x + dx
            node.y = node.y + dy

        # improvements
        self.temperature = math.ceil(self.temperature / 2)

    def iteratePositionOrigin(self):
        self.iterationCount += 1
        self.energy = 0
        # initialize net forces
        for i in range(self.N):
            self.nodes[i].force_x = 0
            self.nodes[i].force_y = 0

        # repulsion between all pairs
        for i1 in range(self.N):
            node1 = self.nodes[i1]
            for i2 in range(i1 + 1, self.N):
                node2 = self.nodes[i2]
                dx = node2.x - node1.x
                dy = node2.y - node1.y
                if dx != 0 or dy != 0:
                    distanceSquared = dx * dx + dy * dy
                    distance = math.sqrt(distanceSquared)
                    force = K_r / distanceSquared * 1.3
                    self.energy += force
                    fx = force * dx / distance
                    fy = force * dy / distance
                    node1.force_x = node1.force_x - fx
                    node1.force_y = node1.force_y - fy
                    node2.force_x = node2.force_x + fx
                    node2.force_y = node2.force_y + fy

        # spring force between adjacent pairs
        for i1 in range(self.N):
            node1 = self.nodes[i1]
            for j in range(0, node1.getNeighborLength()):
                i2 = node1.neighbors[j]
                node2 = self.nodes[i2]
                # 防止重复
                if i1 < i2:
                    dx = node2.x - node1.x
                    dy = node2.y - node1.y
                    if dx != 0 or dy != 0:
                        distance = math.sqrt(dx * dx + dy * dy)
                        force = K_s * (distance - self.L)  # 减去弹簧长度， 胡克定律
                        self.energy += force
                        fx = force * dx / distance
                        fy = force * dy / distance
                        node1.force_x = node1.force_x + fx
                        node1.force_y = node1.force_y + fy
                        node2.force_x = node2.force_x - fx
                        node2.force_y = node2.force_y - fy
        # update positions

        for i in range(self.N):
            node = self.nodes[i]
            dx = self.delta_t * node.force_x
            dy = self.delta_t * node.force_y
            # 减少开方运算，提高速度
            displacementSquared = dx * dx + dy * dy
            if displacementSquared > self.MAX_DISPLACEMENT_SQUARED:
                s = math.sqrt(self.MAX_DISPLACEMENT_SQUARED / displacementSquared)
                dx = dx * s
                dy = dy * s
            node.x = node.x + dx
            node.y = node.y + dy

    def start_ite(self):
        time_start = time.clock()
        while (self.iterationCount < self.MAX_ITERATION):
            self.iteratePosition()
            # self.iteratePositionOrigin()
            if (abs(self.energy) < self.MIN_ENERGY):
                break
        time_end = time.clock()
        print("energy is " + str(self.energy))
        return  time_end - time_start

    def drawPic(self):

        # draw the picture
        pygame.init()
        screen = pygame.display.set_mode((self.height, self.width), RESIZABLE, 24)  # create a window
        # screen = pygame.display.set_mode((height, width ), HWSURFACE | FULLSCREEN, 32)
        pygame.display.set_caption("Force-Direct Layout of Graph")  # 设置窗口标题
        color = (200, 156, 64)
        colorLine = (255, 0, 0)

        while True:
            screen.fill([0, 0, 0])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.iteratePosition()
                    print("energy is " + str(self.energy))

            # drawing
            for i in range(self.nodesNum):
                current = self.nodes[i]
                position = (math.ceil(self.nodes[i].x) + self.offset, math.ceil(self.nodes[i].y) + self.offset)
                for j in range(current.getNeighborLength()):
                    neibor = self.nodes[current.neighbors[j]]
                    neiborPos = (math.ceil(neibor.x) + self.offset, math.ceil(neibor.y) + self.offset)
                    # pygame.draw.line(screen, color, position, position, 21)
                    pygame.draw.line(screen, colorLine, position, neiborPos, 1)
            # 后画点，否则就糊了
            for i in range(self.nodesNum):
                current = self.nodes[i]
                position = (math.ceil(current.x) + self.offset, math.ceil(current.y) + self.offset)
                pygame.draw.circle(screen, color, position, 5, 5)
            # pygame.display.flip()
            pygame.time.delay(20)
            pygame.display.update()



# initialization
# nodes 使用的数据初始化，随机生成
nodes = []
edges = 22  # possibility to generate edge
nodesNum = 111

# nodesNum = [22, 100, 500, 1000, 5000]
nodesNum = [ 700, 500, 100, 22]
# nodesNum = [50, 100]
# nodesNum = [500]
edges =[ math.log(y, 9) for y in nodesNum]

def threadDraw(nodeNum):
    fg = ForceGraph(nodesNum)

threads=[]
for ite in range(len(nodesNum)):
    nodes = []
    # 初始化节点
    for i in range(nodesNum[ite]):
        x = random.random() * nodesNum[ite] * 2
        y = random.random() * nodesNum[ite] * 2
        nodes.append(Node(x, y))
    # 初始化邻居节点
    for i in range(nodesNum[ite]):
        count = math.floor(random.random() * edges[ite])
        nigs = []
        for j in range(count):
            k = math.floor(random.random() * 100 % nodesNum[ite])
            if k != i and k not in nigs:
                nigs.append(k)
        nodes[i].setNeighbor(nigs)
    # print ("create thread "+str(ite))
    threads.append(threading.Thread(target=ForceGraph, args=(nodesNum[ite], nodes)))

for t in threads:
    t.setDaemon(True)
    t.start()
for t in threads:
    t.join()

print("=====end=====")


