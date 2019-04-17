import time

# filter 也是一个迭代器！！ 
def primes():
    def _odd_iter():
        n = 1
        while True:
            n = n + 2
            yield n

    # *** 不能再filter 中间直接写 lambda 
    # n 的变量的范围： 局部还是全局变量
    def _not_divisible(n):
        return lambda x: x % n > 0

    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

t0 = time.time()
li = []
# li1 = []
for i in primes():
    if len(li) == 10000: break
    li.append(i)
t1 = time.time()

# 我的生成 质数函数， 不是生成器的
lip = [2, 3, ]
def iterPrime(p):
    while 1:
        p+=2
        if prime(p):
            return p
def prime(p):
    for l in lip:
        if p%l ==0: return False
    return True
for i in range(10000-2):
    lip.append(iterPrime(lip[-1]))
t2 = time.time()
print('length of lip, li %d %d ' %(len(lip), len(li)))
# with open('prime.json', 'w') as f:
#     f.write(str(li ) +'\n\n\n\n' + str(lip))
print(set(lip) - set(li))
print('=============================')
print(set(li) - set(lip))
print('liaoxuefeng time %f, my time %f' %(t1-t0, t2-t1))
# 前10000个的素数 liaoxuefeng time 9.524563, my time 3.848583