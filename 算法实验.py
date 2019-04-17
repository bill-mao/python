

#%%
import random
def randPartition(A, p, r):
    i = random.randint(p, r)
    # move pivot to the end
    A[r], A[i] = A[i], A[r]
    pivot = A[r]
    i = p-1
    for j in range(p, r):
        if A[j] <= pivot:
            i+=1
            A[i], A[j] = A[j], A[i]
    i+=1            
    A[i], A[r] = A[r], A[i]
    return i

def quickSort(A, p, r):
    if p<r:
        q = randPartition(A, p, r)
        quickSort(A, p, q-1)
        quickSort(A, q+1, r)

# delete same value too much recursively calls problem
def quickSort2(A, p, r):
    if p<r:
        q = randPartition(A, p, r)
        # q is biggest same value position
        low = q 
        while low>=p and A[low]==A[q]: 
            low-=1
        quickSort(A, p, q-1)
        quickSort(A, q+1, r)


#%%
# 1000 个random小样本测试： assert
# 排序的长度为0-1000
import operator
for i in range(1000):
    length = random.randint(0, 1000)
    li = [random.randint(-1000, 1000) for j in range(length)]
    sortedLi = sorted(li)
    quickSort(li, 0, len(li)-1)
    assert operator.eq(sortedLi, li)
    
#%%
# question 1
# 1e6 32int 性能测试
import time
st = time.time()
length = int(1e6)
iterTime = 3
for i in range(iterTime):
    li = [random.randint(-(1<<31), (1<<31)-1) for j in range(length)]
    quickSort(li, 0, len(li)-1)
end = time.time()
span = (end - st)/iterTime
print("average time of sort 1e6 32 int num is %f" %span)
# 11 seconds


#%%
# question 2
# 令输入为 1000000 个 1，记录算法的运行表现
import time
st = time.time()
iterTime = 3
size = list(map(int, []))
for i in range(iterTime):
    li = [1 for i in range(int(1e6))]
    quickSort(li, 0, len(li)-1)
end = time.time()
span = (end - st)/iterTime
print("average time of sort 1e6's '1'  is %f" %span)


#%%
# question3
# 保持输入规模为 10000，先向数组中添加 x%比例的 1，再向数组中加入随机 32 位整数直到填满数组。
# 分别令 x=50，60，70，80，90，100，记录算法的运行表现。 


#%%
# question4
# 分别令输入规模为 1000，5000，重复第(3)步的实验。 
# (5) (选做)  调用你所用的程序设计语言中自带的快速排序算法，如 c++ STL 中的 sort 或 qsort，
# 观察它们对上述输入有没有无法得出结果的情况出现。

'''
4.1  思考并解决问题 
按照算法导论中给出的伪代码实现的算法会在某些输入下无法得出结果。思
考并回答：这种问题是如何产生的？如何解决？按照你的思路修改你的实现的快
速排序算法，解决这一问题。'''


# convex hull
# 4.1  实现基于枚举方法的凸包求解算法 
# 提示：考虑 Q 中的任意四个点 A、B、C、D，如果 A 处于 BCD 构成的三角
# 形内部，那么 A 一定不属于凸包 P 的顶点集合。 
# 把得到的点结合按照逆时针输出
def bruteForceConvexHull(Q):
    # range check 
    if len(Q) <3: return len(Q)
    hull = set(Q)
    # 4 loops to delete point in the triangle
    length = len(Q)
    for i in range(length):
        for j in range(i+1, length):
            for k in range(j+1, length):
                for P in Q: # in hull??
                    if P in hull and inTriangle(Q[i], Q[j], Q[k], P):
                        hull.remove(P)
    
    # find leftes and rightest, sort to output
    leftest, rightest = min(hull), max(hull)
    hull.remove(leftest)
    hull.remove(rightest)
    up, down = [], []
    # 一定没有共线点
    for h in hull:
        if crossProduct(vector(leftest, rightest), vector(leftest, h)):
            up.append(h)
        else: down.append(h)
    return [leftest]+ sorted(up)+sorted(down, reversed = True) + [rightest]



# 4.2  实现基于 Graham-Scan 的凸包求解算法 
# 提示：具体算法思想见课件。 
import math

# 计算arctan 有点慢
def theta(p1, p2):
    deltaX, deltaY = p2[1]-p1[1], p2[0]-p1[0]
    # 90 degree
    if deltaX == 0:
        # assuming no coincide point
        if p2[1]>p1[1]: return math.pi/2  
        else : return math.pi *3/2
    # the arctan
    tan = (deltaX)/(deltaY)
    arc = math.atan(tan)
    if deltaX< 0:
        return math.pi + arc 
    elif deltaY >=0: return arc 
    else: return 2* math.pi + arc 

def euclideanSquare(p1, p2):
    deltaX, deltaY = p2[1]-p1[1], p2[0]-p1[0]
    return deltaX**2 + deltaY**2

def crossProduct(vec1, vec2):
    return vec1[0]*vec2[1] - vec1[1]*vec2[0]

# A point to B
def vector(A, B):
    return (B[0]-A[0], B[1]-A[1])

# include edge**
def inTriangle(A, B, C, P):
    # in the same side 
    # optimize: clockwise: calculate 3 cross product 
    '''t1 = PA^PB,
    t2 = PB^PC,
    t3 = PC^PA,
    如果t1，t2，t3同号（同正或同负），那么P在三角形内部，否则在外部。'''
    PA, PB, PC = vector(P, A),vector(P, B),vector(P, C), 
    c1 = crossProduct(PA, PB)
    c2 = crossProduct(PB, PC)
    c3 = crossProduct(PC, PA)
    if c1>=0 and c2>=0 and c3>=0 or\
        c1<=0 and c2<=0 and c3<=0 :
        return True 
    else: return False

# assuming no coincide points
# change in place, return size
def grahamScan(Q):
    # range check:
    if len(Q) < 3: return len(Q)
    # find one lowest, leftest point p0 
    p0 = min(Q, key= lambda q:(q[1], q[0])) 
    # set p0 as polar coordinate, and sort the point in Q
    Q.sort(key= lambda q: (theta(p0,q), euclideanSquare(q, p0)))
    index = 1
    for i in range(2, len(Q)):
        # if anti-clockwise (cross product : not include line: 0!!) then include, else swap(means pop)
        # A, B, C = Q[index-1], Q[index], Q[i]
        # while crossProduct(vector(A, B), vector(B, C)) <=0:
        while crossProduct(vector(Q[index-1], Q[index]), vector(Q[index], Q[i]) )  <=0:
            index-=1
        # add in
        index+=1
        Q[index], Q[i] = Q[i], Q[index]
    return index+1



# 4.3  实现基于分治思想的凸包求解算法 
# 提示：具体算法思想见课件。 



# 4.4  对比三种凸包求解算法 
# （1）实现随机生成正方形(0,0)-(0,100)-(100,100)-(100,0)内的点集合 Q 的算法； 
# （2）利用点集合生成算法自动生成大小不同数据集合，如点数大小分别为(1000，2000，3000…)的数据集合； 
import random as rd 
def generateQ(x1=0, x2=100, y1=0, y2=100, size=1000 ):
    li = [(rd.randint(x1, x2), rd.randint(y1, y2))  for i in range(size) ]
    return list(set(li))
# （3）对每个算法，针对不同大小的数据集合，运行算法并记录算法运行时间； 
# （4）对每个算法，绘制算法性能曲线，对比算法。 



# import numpy as np
import matplotlib.pyplot as plt
#X轴，Y轴数据
x = [0,1,2,3,4,5,6]
y = [0.3,0.4,2,5,3,4.5,4]
plt.figure(figsize=(8,4)) #创建绘图对象
plt.plot(x,y,"b--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.plot(x,y,"--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.plot(x,y,"b--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

plt.xlabel("datasize(s)") #X轴标签
plt.ylabel("time (s)")  #Y轴标签
plt.title("Convex Hull : ") #图标题
plt.show()  #显示图
plt.savefig("line.jpg") #保存图


