



数个数： itertools.groupby; re
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













        


#=================  ccf 201803-2  碰撞的小球 =================
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
    

#================= 牛客 2017校招真题在线编程 - 合唱团。能力值排行
    n = int(input())
    arr =  [int(i) for i in input().strip().split(' ')]
    k,d  = map(int, input().strip().split(' '))

    #ends 小于 k 的最大值
    fmax = [[0 for i in range(n)] for j in range(k)]
    fmin = [[0 for i in range(n)] for j in range(k)]

    # initialization 
    for i in range(n):
        fmax[0][i] = fmin[0][i] = arr[i]

    # k can be larger than n
    res = arr[0]
    for i in range(0,n) :
        for j in range(1,k):
            # max(i-d, 0)-1， 结尾为 -1 ！！ 很重要
            for a in range(i-1, max(i-d, 0)-1, -1):
                fmax[j][i] = max(fmax[j][i], max(fmax[j-1][a] * arr[i], fmin[j-1][a] * arr[i]))
                fmin[j][i] = min(fmin[j][i], min(fmax[j-1][a] * arr[i], fmin[j-1][a] * arr[i]))
                # fmax[j][i] = max(fmax[j][i], max(fmax[a][i-1] * arr[i], fmin[a][i-1] * arr[i]))
                # fmin[j][i] = min(fmax[j][i], min(fmax[a][i-1] * arr[i], fmin[a][i-1] * arr[i]))
                # print(fmax)
            # k可能等于1！ 内部那个循环就不会执行
            # res2 = max(res2, fmax[j][i])
        res = max(res, fmax[k-1][i])
            
    print(res)


网络： 优雅的方式获取本机IP
    import socket
    def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
    print(get_host_ip())


=============未解决




#===========url 2018-10-11： 60分 依旧没有解决


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