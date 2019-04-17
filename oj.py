
'''
any， itertools 的巧妙使用
    dp.append(any(dp[j] and s[j:i] in wordDict for j in range(i)))
    memo[i] = [s[i:j] + (tail and ' ' + tail)
               for j in [i + x for x in ss]
               if s[i:j] in wordDict
               for tail in sentences(j)]


# 数个数： itertools.groupby; re
    Solution 1 ... using a regular expression

    def countAndSay(self, n):
        s = '1'
        for _ in range(n - 1):
            s = re.sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1), s)
        return s
    Solution 2 ... using a regular expression

    def countAndSay(self, n):
        s = '1'
        for _ in range(n - 1):
            s = ''.join(str(len(group)) + digit
                        for group, digit in re.findall(r'((.)\2*)', s))
        return s
    Solution 3 ... using groupby

    def countAndSay(self, n):
        s = '1'
        for _ in range(n - 1):
            s = ''.join(str(len(list(group))) + digit
                        for digit, group in itertools.groupby(s))
        return s
'''



#表示数值的字符串 牛客
def isNumeric(self, s):
    # test cases
    # "123.45e+6", "", 
    import re
    pure = re.compile(r"\d+$")     #**$$$ 
    # sign = re.compile(r"(+|-){0,1}\d+$")
    sign = re.compile(r"(\+|-){0,1}\d+$")
    s = s.lower()
    
    def isDecimal(s):
        if s.count('.') == 1:
            front, behind = s.split('.')
            print( sign.match(front) , pure.match(behind) )
            ###
            return (sign.match(front) is not None or \
                re.match(r"(\+|-){0,1}$", front ) is not None) \
                    and  pure.match(behind) is not None
        return False
    def isDigit(s):
        return sign.match(s) is not None
    def isE(s):
        if s.count('e') == 1 :
            front, behind = s.split('e')
            print( isDigit(front) , isDecimal(front) ,isDigit(behind)  )
            return (isDigit(front) or isDecimal(front)) and isDigit(behind)
        return False
    return isE(s) or isDecimal(s) or isDigit(s)

# 131. Palindrome Partitioning
def partition(self, s: str) -> List[List[str]]:
    n = len(s)
    if n == 0: return []
    
    def backtrack(st, cur, partitions):
        if n == st: 
            partitions.append(cur)
            return
        for i in range(st, n):
            candidate = s[st:i+1] 
            if candidate == candidate[::-1]:
                backtrack(i+1, list(cur) + [candidate] , partitions)
    out = []
    backtrack(0, [], out)
    return out

#同一类问题，触类旁通
# DP 状态方程，把握问题和子问题之间的状态转移关系； 分析
def findTargetSumWays(self, nums, S):
    total = sum(nums)
    A = total + S
    if total < abs(S) or A % 2 == 1:
        return 0
    A = A // 2
    count = [0] * (A + 1)
    count[0] = 1
    partial = 0
    for n in nums:
        partial += n
        for i in range(min(A, partial), n-1, -1):
            count[i] += count[i - n]
    return count[A]

# walk around : % 求余有很多的数学性质
def subarraysDivByK(self, A: List[int], K: int) -> int:
    count = [0 for i in range(K)]
    count[0] = 1
    out = 0
    acc = 0
    for i in A:
        acc = (acc+i)%K
        out+=count[acc] 
        count[acc%K]+=1
    return out 


    


    def beautifulArray(self, N: int) -> List[int]:
        res = [1] 
        
        while len(res)< N:
            res = [i*2-1 for i in res]+[2*i for i in res]
        return [i for i in res if i<=N ]

        1. Deletion
        Easy to prove.

        2. Addition
        If we have A[k] * 2 != A[i] + A[j],
        (A[k] + x) * 2 = A[k] * 2 + 2x != A[i] + A[j] + 2x = (A[i] + x) + (A[j] + x)

        E.g: [1,3,2] + 1 = [2,4,3].

        3. Multiplication
        If we have A[k] * 2 != A[i] + A[j],
        for any x != 0,
        (A[k] * x) * 2 = A[k] * 2 * x != (A[i] + A[j]) * x = (A[i] * x) + (A[j] * x)

        E.g: [1,3,2] * 2 = [2,6,4]        

# 矩阵打印： 不一定要很复杂
def printMatrix(self, matrix):
    res = []
    while matrix:
        res += matrix.pop(0)
        if matrix and matrix[0]:
            for row in matrix:
                res.append(row.pop())
        if matrix:
            res += matrix.pop()[::-1]
        if matrix and matrix[0]:
            for row in matrix[::-1]:
                res.append(row.pop(0))
    return res

# 找数字序列中 1 的个数
def NumberOf1Between1AndN_Solution(self, n):
    # write code here
    # range check 
    if n<1: return 0
    # pattern: kth pos of number's "1"; sum up
    count = 0
    for k in range(1, len(str(n))+1):
        count += 10**(k-1) * (n//10**k) 
        # corner value
        left = max(0, n%10**k- 10**(k-1) +1)
        left = min(left, 10**(k-1))
        count += left
    return count

'''
Runtime: 36 ms, faster than 99.35% of Python3 online submissions for Find Minimum in Rotated Sorted Array II.
Memory Usage: 13.5 MB, less than 5.63% of Python3 online submissions for Find Minimum in Rotated Sorted Array II. 都差不多，其实
'''
def findMin(self, nums: List[int]) -> int:
    st, end = 0, len(nums)-1
    # range check
    if nums[st] < nums[end]: return nums[0]
    while st+1<end:
        mid = (st+end)//2
        if nums[mid] == nums[st] == nums[end]:
            # linear search 
            return min(nums[st:end+1])
        # if nums[mid]> nums[st] :
        # corner value : ==  ： 剑指offer 上面更简单的判定，再看**
        if nums[mid]> nums[st] or nums[mid] > nums[end]:
            st = mid
        elif nums[mid] < nums[end] or nums[mid] < nums[st]:
            end = mid
    return min(nums[st], nums[end])

# 没有相等的数的二分搜素
def findMin(self, nums: List[int]) -> int:
    if not nums:
        return -1
    start, end = 0, len(nums) - 1
    while start + 1 < end:
        mid = (start + end) // 2
        if nums[mid] < nums[end]:
            end = mid
        else:
            start = mid
    return min(nums[start], nums[end])


#=================  ccf 201803-2  碰撞的小球 =================
def bumpBall():
    # 方程的等式： 相对位置不改变
    n, L, t = map(int, input().split())
    tmp = list(map(int, input().split()))
    arr = [(i,j) for i, j in enumerate(tmp)]

    # sort the arr, get the real output order
    arr = sorted(arr, key= lambda x:x[1],)
    # out_order[i] = j means j'th place should be output in i'th turn
    out_order = [0 for i in range(n)]
    for i,v in enumerate(arr):
        out_order[v[0]] = i

    # update the bumped place
    for i in range(n):
        cur = tmp[i] + t
        # next place
        cur = cur%(2*L)
        # better way?
        if cur > L:
            cur = 2*L - cur

        tmp[i] = cur

    out = sorted(tmp)

    for i in out_order[:-1]:
        print(str(out[i]) + ' ', end = '')
    #print(out[-1])
    print(out[out_order[-1]])
    


'''
#===========url 2018-10-11： 60分 依旧没有解决
    # 最新 90 分 2019-4-17
    # 写代码的速度变快了，不到一小时吧
    # 代码更加规范了**
    # Python更加熟练了

    import re

    legalPattern = re.compile(r"(\w|[-.])+")
    n, m = map(int, input().strip().split())
    patterns = []
    # read pattern
    for i in range(n):
        patterns.append(input().strip().split())

    # return str or None
    def match(p, s):
        if p[-1] == '/' and p[0] != '/': p = p[:-1]
        if s[-1] == '/' and s[0] != '/': s = s[:-1]

        li = p.split("/")[1:]
        lis = s.split("/")[1:]
        arguments = []
        # length of two list might be different
        # the right one is always pattern <= s 
        ## last /??
        if len(lis) < len(li) : return None 
        if len(lis) > len(li) and '<path>' not in li: return None 
        for i,v in enumerate(li):
            ss = lis[i]
            if v == "<path>":
                arguments.append("/".join(lis[i:]))
            elif v == "<int>" :
                if ss.isdigit():
                    # 00
                    ss = str(int(ss))
                    arguments.append(ss)
                else: return None
            elif v == "<str>":
                arguments.append(ss)
            elif v == ss:
                pass
            else: return None
        return ' '.join(arguments)

    for i in range(m):
        s = input().strip()
        for p in patterns:
            out = match(p[0], s)
            if out is not None: 
                if len(out)>0:
                    print(p[1], out) 
                else: print(p[1])
                break
        else: print("404")

    5 4
    /articles/2003/ special_case_2003
    /articles/<int>/ year_archive
    /articles/<int>/<int>/ month_archive
    /articles/<int>/<int>/<str>/ article_detail
    /static/<path> static_serve
    /articles/2004/
    /articles/1985/09/aloha/
    /articles/hello/
    /static/js/jquery.js

    测试用例：
        很重要，简直让人崩溃啊，这道题目实在是不想再做了。。。。
      



    n, m = map(int, input().split())
    rules = [] # ele: [[ ], name]
    import re 
    digit = re.compile(r'\d+')
    string = re.compile(r'[\w\-_.]+')


    for i in range(n):
        url, name = input().split()
        url = url.split('/')
        if url[-1] == '' :
            url.pop(-1)

        rules.append( [url, name])

    for i in range(m):
        words = input().split('/')
        if words[-1] =='':
            words.pop(-1)


        for rule in rules:
            args = []
            finded = 1 # default 1 means matched the rules pattern

            lenr = len(rule[0])
            lenw = len(words)
            # generally if existed, lenr should be <= lenw +1

            # not find
            ## path short / ??
            ## end '/' solved 
            if lenr < lenw and '<path>' not in rule[0]  or lenr > lenw:
                finded = 0
                continue

            for j in range(lenr):
                r = rule[0][j]
                w = words[j]

                if r == '<int>' :
                    if digit.match(w):
                        ##
                        args.append(str(int(w)))
                        continue
                    else:
                        finded = 0
                        break
                elif r == "<str>" : 
                    if string.match(w):
                        args.append(w)
                        continue
                    else:
                        finded =0;
                        break
                elif r =='<path>' :
                    args.append('/'.join(words[j:]))
                    ### 
                    finded = 1
                    break
                elif r != w:
                    finded = 0
                    break
                #else:
                #    args.append(w)


            if finded == 1:
                break

        if finded:
            print(rule[1], ' '.join(args))
        else:
            print('404')


'''            