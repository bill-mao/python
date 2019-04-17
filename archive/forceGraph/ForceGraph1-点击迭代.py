import random
import math

import pygame
from pygame.locals import *  #导入一些常用的函数和常量
from sys import exit  #向sys模块借一个exit函数用来退出程序

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.force_x =0
        self.force_y =0

    def getNeighborLength(self):
        return len(self.neighbors)
    def setNeighbor(self, neighbors):
        self.neighbors = neighbors
    def addNeighbor(self, i):
        self.neighbors.append(i)

def nodeInitialize(edges, nodesNum, nodes):
    # 初始化节点
    for i in range(nodesNum):
        x = random.random() * 100
        y = random.random() * 100
        nodes.append(Node(x, y))
    # 初始化邻居节点
    for i in range(nodesNum):
        count = math.floor(random.random() * edges)
        nigs = []
        for j in range(count):
            k = math.floor(random.random() * 100 % nodesNum)
            if k != i and k not in nigs:
                nigs.append(k)
        nodes[i].setNeighbor(nigs)

edges = 22 # possibility to generate edge
nodesNum = 50

L = 222 # spring rest length 弹簧的初始长度
# K_r = 333 # repulsive force constant
K_s = 111 # spring constant
delta_t = 3 # time step， 值可以动态设置，刚开始大一点- 运行速度快；后面慢一点，保证能够收敛
MAX_DISPLACEMENT_SQUARED = 20 # 缓冲，防止一下子运动太多的距离
#改进算法
temperature = 20 #让delta_t能够动态改变大小, 随着迭代次数增加，不断减少
iterationCount = 0 #随着迭代的次数增加而下降  temperature = temperature / 1.2
farDistance = 200 #当超过这个值的时候，斥力就不计算了，优化运行速度

ratio = 2 # 由用户设置，根据产生的图的形状来调整参数
K_r = K_s * ratio
randomForce = 2.5
#画图到里面去了
offset= 400
height = 888
width = 999

# initialization
# nodes 使用的数据初始化，随机生成
nodes = []
nodeInitialize(edges, nodesNum, nodes)
N = nodesNum

def iteratePosition( ):
    global temperature
    # initialize net forces
    for i in range(N):
        nodes[i].force_x = 0
        nodes[i].force_y = 0

    # repulsion between all pairs
    for i1 in range(N):
        node1 = nodes[i1]
        for i2 in range(i1 + 1, N):
            node2 = nodes[i2]
            dx = node2.x - node1.x
            dy = node2.y - node1.y
            if dx > farDistance or dy > farDistance:
                continue
            if dx != 0 or dy != 0:
                distanceSquared = dx * dx + dy * dy
                distance = math.sqrt(distanceSquared)
                force = K_r / distanceSquared
                fx = force * dx / distance
                fy = force * dy / distance
                node1.force_x = node1.force_x - fx
                node1.force_y = node1.force_y - fy
                node2.force_x = node2.force_x + fx
                node2.force_y = node2.force_y + fy
            # ***产生一个随机的small的力，保证在两个重合节点有相同的邻居时候能够运动
            else:
                fx = random.random() * randomForce
                fy = random.random() * randomForce
                node1.force_x = node1.force_x - fx
                node1.force_y = node1.force_y - fy
                node2.force_x = node2.force_x + fx
                node2.force_y = node2.force_y + fy

    # spring force between adjacent pairs
    for i1 in range(N):
        node1 = nodes[i1]
        for j in range(0, node1.getNeighborLength()):
            i2 = node1.neighbors[j]
            node2 = nodes[i2]
            # 防止重复
            if i1 < i2:
                dx = node2.x - node1.x
                dy = node2.y - node1.y
                if dx != 0 or dy != 0:
                    distance = math.sqrt(dx * dx + dy * dy)
                    force = K_s * (distance - L)  # 减去弹簧长度， 胡克定律
                    fx = force * dx / distance
                    fy = force * dy / distance
                    node1.force_x = node1.force_x + fx
                    node1.force_y = node1.force_y + fy
                    node2.force_x = node2.force_x - fx
                    node2.force_y = node2.force_y - fy
    # update positions
    for i in range(N):
        node = nodes[i]
        # 动态改变delta_t，刚开始快，后来慢，保证收敛
        dx = temperature * delta_t * node.force_x
        dy = temperature * delta_t * node.force_y
        # 减少开方运算，提高速度
        displacementSquared = dx * dx + dy * dy
        if displacementSquared > MAX_DISPLACEMENT_SQUARED:
            s = math.sqrt(MAX_DISPLACEMENT_SQUARED / displacementSquared)
            dx = dx * s
            dy = dy * s
        node.x = node.x + dx
        node.y = node.y + dy

    #improvements
    temperature = temperature / 1.2

#draw the picture
pygame.init()
screen = pygame.display.set_mode((height, width ), 0, 32) #create a window
pygame.display.set_caption("Force-Direct Layout of Graph") #设置窗口标题
color = (200, 156, 64)
colorLine = (255, 0, 0)

while True:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            iteratePosition()

    #drawing
    for i in range(nodesNum):
        current = nodes[i]
        position = (math.ceil(nodes[i].x) + offset, math.ceil(nodes[i].y) + offset)
        for j in range(current.getNeighborLength()):
            neibor = nodes[current.neighbors[j]]
            neiborPos = (math.ceil(neibor.x) + offset , math.ceil(neibor.y) + offset)
            # pygame.draw.line(screen, color, position, position, 21)
            pygame.draw.line(screen, colorLine, position, neiborPos, 1 )
    #后画点，否则就糊了
    for i in range(nodesNum):
        current = nodes[i]
        position = (math.ceil(nodes[i].x) + offset, math.ceil(nodes[i].y) + offset)
        pygame.draw.circle(screen, color, position, 5, 5)
    # pygame.display.flip()
    pygame.time.delay(20)
    pygame.display.update()


