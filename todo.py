


ans = 0
ans+= n//10 + (n%10)//5 + n%5//2 + n%2


# 基于cache递归的动态规划
#dp[i][j] 表示从原点到Mij 的最短距离
dp = [
    [-1 for i in range layer[l]]
    for l in range(lenLayers)
]

def shortestDistance(i, j):
    if dp[i][j] != -1: 
        return dp[i][j]
    dp[i][j]=  min([shortestDistance(i-1, k) + distance((i-1,k), (i,j)) for k in layer[i-1]])
    return dp[i][j]



# 初始状态
for i in range(n):
    dp[n-1][i] = 0 if A[n-1][i] ==0 else 1
    dp[i][n-1] = 0 if A[i][n-1] ==0 else 1
# 状态转移方程    
Dp[i][j] = 0 if A[i][j] ==0 else min( [dp[i+1][j] , dp[i][j+1] , dp[i+1][j+1] ]) +1


def minDistance( word1, word2):
    if not word1 and not word2:
        return 0
    if not word1:
        return len(word2)
    if not word2:
        return len(word1)
    if word1[0] == word2[0]:
        return minDistance(word1[1:], word2[1:])
    insert = 1 + minDistance(word1, word2[1:])
    delete = 1 + minDistance(word1[1:], word2)
    replace = 1 + minDistance(word1[1:], word2[1:])
    return min(insert, replace, delete)


# 数组越界的值设置为 0 
maxcake[time][position] = 
    max(
        fallcake[time][position],
        fallcake[time][position+1],
        fallcake[time][position-1],
        ) + 
    max(
        maxcake[time-1][position],
        maxcake[time-1][position-1],
        maxcake[time-1][position+1],
    )





当n<m时，由于划分中不可能出现负数，因此就相当于g(n,n)；
当n>m时，根据划分中是否包含m，可以分为两种情况：
    划分中包含  的情况，即{m,{x1,x2,x3,...,xi}}，其中{x1,x2,x3,...,xi}的和为n-m，
    可能再次出现m，因此是（n-m）的m划分，因此这种划分个数为g(n-m,m)；

    划分中不包含m的情况，则划分中所有值都比m小，即n的（m-1）划分，个数为g(n,m-1)；
因此，g(n,m)=g(n-m,m)+g(n,m-1) 。



k = i//j
count[i - k*j][0] =0
for x in range(1,j):
    count[i-k*j][x] = count

jump = m 
for i in range(start, n, jump)

# initialization
for j in range(1, n):
    split[1][j] = 0 
    split[j][1] = j

for i in range(1, n):
    for j in range(1, n):
        if j>=i: 
            split[i][j] = split[i][j-1]
        else:
            split[i][j] = split[i][j-1] + split[i-j][j]





# 环+ 做少的礼物： coding 的能力： 知道了算法之后







# merge sort
def merge(li, l, mid, r ):
    copylist =  li[l:r+1]
    # c语言里面是开辟了一个全局变量，一整个数组，所以下标能够和li 一致
    # ll, rr = l, r 
    i, j, cur= l, mid+1, l
    # while l<mid+1 and r>mid:
    while i<mid+1-l and j < r+1-l:
        if copylist[l-ll] < copylist[j]:
            li[cur] = copylist[i]
        else:
            li[cur] = copylist[j]
        cur+=1
    while i<mid+1-l:
        li[cur] = copylist[l-ll]
        l+=1
        cur+=1
    while j< r+1-l:
        li[cur] = copylist[r-ll]
        r-=1
        cur+=1

def mergeSort(li, l, r):
    # if l ==r: return
    if l<r:
        mid = (l+r)//2
        mergeSort(li, l, mid)
        mergeSort(li, mid+1, r)
        merge(li, l, mid, r)





# heapsort P298









# quick sort
def partition(array, st, end):
    # if end==st:
    #     return st 
    # first , pivot = st, array[st]
    pivot = array[st]
    # st+=1
    while st< end:
        # while st< end and array[end]>pivot:   
        # >= !!!
        while st<end and array[end[ >= pivot]:
            end-=1
        array[st] = array[end]
        while  st < end and array[st]<pivot:
            st+=1
        array[end] = array[st]
    #st == end in the end???
    array[end ] = pivot
    return end 

def qsort(array, st, end):
    # if st == end: return\
    if st<end:
        index = partition(array, st, end)
        # qsort(array, st, index)
        qsort(array, st, index-1)
        qsort(array, index+1, end)













































快
        int hold1 = Integer.MIN_VALUE, hold2 = Integer.MIN_VALUE;
        int release1 = 0, release2 = 0;
        for(int i:prices){                              // Assume we only have 0 money at first
            release2 = Math.max(release2, hold2+i);     // The maximum if we've just sold 2nd stock so far.
            hold2    = Math.max(hold2,    release1-i);  // The maximum if we've just buy  2nd stock so far.
            release1 = Math.max(release1, hold1+i);     // The maximum if we've just sold 1nd stock so far.
            hold1    = Math.max(hold1,    -i);          // The maximum if we've just buy  1st stock so far. 
        }
        return release2; ///Since release1 is initiated as 0, so release2 will always higher than release1.
                
        DP 所有的K = 2,3,4 的解； 通用解法        
class Solution {
public:
    int maxProfit(vector<int> &prices) {
        // f[k, ii] represents the max profit up until prices[ii] (Note: NOT ending with prices[ii]) using at most k transactions. 
        // f[k, ii] = max(f[k, ii-1], prices[ii] - prices[jj] + f[k-1, jj]) { jj in range of [0, ii-1] }
        //          = max(f[k, ii-1], prices[ii] + max(f[k-1, jj] - prices[jj]))
        // f[0, ii] = 0; 0 times transation makes 0 profit
        // f[k, 0] = 0; if there is only one price data point you can't make any money no matter how many times you can trade
        if (prices.size() <= 1) return 0;
        else {
            int K = 2; // number of max transation allowed
            int maxProf = 0;
            vector<vector<int>> f(K+1, vector<int>(prices.size(), 0));
            for (int kk = 1; kk <= K; kk++) {
                int tmpMax = f[kk-1][0] - prices[0];
                for (int ii = 1; ii < prices.size(); ii++) {
                    f[kk][ii] = max(f[kk][ii-1], prices[ii] + tmpMax);
                    tmpMax = max(tmpMax, f[kk-1][ii] - prices[ii]);
                    maxProf = max(f[kk][ii], maxProf);
                }
            }
            return maxProf;
        }
    }
};

```