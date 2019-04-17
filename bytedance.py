










# ===================== 数字序列找某一位的数
# % // +-1 之类的还是不熟练
# 稍微仔细一点就能够写出来的！！2019-4-15： 不要急于调试，先看看自己代码，
# 每个符号什么类型，什么意思



def search(t):
    s =''.join(map(str, range(t)))
    # print(s)
    i = int(s[t-1])
    return i

def search2(t):
    # find the corresponding number 
    # t t  shadow variable??
    # edge value
    if t<11: return t-1
    bound = 10
    for i in range(1, t):
        if t <= bound: break
        bound += (i+1)*9*10**i 
    # target number is i length***
    # find the order in range of i length
    order = t - bound + i*9*10**(i-1) # order >=1
    targetNum = 10**(i-1)+ (order-1)//i
    # print(targetNum)
    ans = str(targetNum)[order% i -1]
    return int(ans )

import random
for i in range(100):
    t = random.randint(1, 11111)
    if not search2(t) == search(t):
        print(t, search(t), search2(t))

testcases = [10, 11, 12, 2890, 2891, 2892, 2894, 2895]
ans = [9, 1, 0, 9, 1, 0, 0, 1]
#test
for t, a in zip(testcases, ans):
    if search2(t) != a: 
        print(t, a , search(t), )



