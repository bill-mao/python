#!/usr/bin/python
#-*- coding:utf-8 -*-
import itertools
import math
import sys 
def get_cur_info():
    print sys._getframe().f_code.co_filename  # 当前文件名
    print sys._getframe(0).f_code.co_name  # 当前函数名
    
    print sys._getframe(1).f_code.co_name # 调用该函数的函数的名字，如果没有被调用，则返回module

    print sys._getframe().f_lineno # 当前行号


# top triangle valid
mapT1 =   [
	[-1,1,0,0,0,1,1],
	[1,-1,1,0,0,1,0],
	[0,1,-1,0,0,0,1],
	[0,0,0,-1,1,0,1],
	[0,0,0,1,-1,1,0],
	[1,1,0,0,1,-1,1],
	[1,0,1,1,0,1,-1]
]

mapT2 = [[-1, 1, 1, 0, 0, 1, 1], [1, -1, 1, 0, 1, 1, 0], 
[1, 1, -1, 0, 0, 0, 1], [0, 0, 0, -1, 1, 1, 1], 
[0, 1, 0, 1, -1, 1, 1], [1, 1, 0, 1, 1, -1, 1], 
[1, 0, 1, 1, 1, 1, -1]]



half=[
  [-1,1,1,0,0,1,1],
  [0,-1,1,0,1,1,0],
  [0,0,-1,0,0,0,1],
  [0,0,0,-1,1,1,1],
  [0,0,0,0,-1,1,1],
  [0,0,0,0,0,-1,1] ,
[0,0,0,0,0,0,-1]
]


# def change(map):
#   row = len(map)
#   for i in range(0,row):
#     for j in range(0,i):
#       map[i][j] = map [j][i]
#   return map

# print change(half)


def valid(map):
    row = len(map)
    col = len(map[0])
    if(not row == col):
        raise Exception("row col not match")
    for i in range(0,row):
        for j in range(0,row):
            if( not map[i][j] == map[j][i]):
                print ("i , j is :",i ,j)
                return 0
                # forget to take another situation into consideration
            else: return 1



def newFriend(mapT1,mapT2):
    row = len(mapT1)
    friend = [ ]
    for i in range(0,row-1):
        for j in range(i+1,row):
            if(mapT1[i][j]+mapT2[i][j] == 1): 
                print i,j,"  ",mapT2[i][j], "  map1",mapT1[i][j]
                friend.append([i,j])
            else: print "------------------------", i,j,"  ",mapT2[i][j], "  map1",mapT1[i][j]
    return friend



#2list  --- mnd :mutualfriends number 2list

# def countMutualNum(2list map1,2list map2 , int vet1, int vet2)  计算两个人（vet ex） 的共同好友个数
def countMutualNum(map,vet1,vet2):
    row = len(map)
    count=0
    for i in range(0,row):
        if(map[vet1][i] == 1 and map[vet2][i] == 1):
            count+=1
    return count

#计算概率，综合方法
def possible(mapT1,mapT2):
    row = len(mapT1)
    col = len(mapT2)
    if not row == col :
        raise Exception("two map col row are wrong")

    count = 0
    friNum2NewFriNum={}

    for i in range(0,row):
        for j in range(i+1,col):
            if mapT1[i][j] == 0:
                count+=1
                if(mapT2[i][j] == 1):
                    value = countMutualNum(mapT1,i,j)
                    print "common fri value is ",value,"i  j is ",i,j
                    # sdfas???
                    if  value not in friNum2NewFriNum.keys():
                        friNum2NewFriNum[value]=1
                    else: friNum2NewFriNum[value] +=1

    count = count + 0.0
#浮点数的问题
    for i in friNum2NewFriNum:
        print "共同好友个数",i," num ,count, possibility is ",friNum2NewFriNum[i],count,friNum2NewFriNum[i]/count




def convergency(map):
    row = len(map)

    for i in range(0,row):
        numFri = 0
        count =0
        fri =[]
        for k in range(0,row):
            if(map[i][k] == 1):
                fri.append(k)
                numFri+=1
        if(numFri == 0 or numFri == 1):
            print "people i 没有聚集系数 ，朋友数为1 or 0"
        else:
            for f in range(0,numFri):
                for fi in range(f+1,numFri):
                    # if(map[f][fi] == 1):   ^^^^^^^^
                    if(map [fri[f] ] [fri[fi]]  == 1):
                        count+=1
            count += 0.0
            converg = count /(numFri * (numFri-1)/2)

            # print "****fri []is "
            # for aaa in range(0,len(fri)):
            #     print fri[aaa]
            # print "-------------count is ",count
            print "people ",i," convergence is ",converg


possible(mapT1,mapT2)
# convergency(mapT1)

# import pdb
# pdb.set_trace()

# convergency(mapT2)








