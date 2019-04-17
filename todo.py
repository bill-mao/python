



# 环+ 做少的礼物： coding 的能力： 知道了算法之后






def qsort(li:list, st:int, end:int, type = 0):

    if st >= end: return
    def partition(li, st, end):
        pivot = li[st]
        st+=1
        while st<end:
            while st< end and li[end]>=pivot:
                end -=1 
            li[st] = li[end]
            while st<end and li[st] <= pivot: st+=1
            li[end] = li[st]
        li[end] = pivot 
        return end
    index = partition(li, st, end)
    qsort(li, st, index-1)
    qsort(li, index+1, end)
  
# merge sort
def merge(li, l, mid, r ):
    copylist =  li[l:r+1]
    # c语言里面是开辟了一个全局变量，一整个数组，所以下标能够和li 一致
    # ll, rr = l, r 
    i, j, cur= l, mid+1, l
    # while l<mid+1 and r>mid:
    ll =0
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

li = [3, 4, 9, 1, 3, 9]
import random as rd 
for i in range(10):
    length = rd.randint(0, 1000)
    test = [rd.randint(-999, 999) for j in range(length)]
    mergeSort(test, 0, len(test) -1)
    print(test)
    assert(all([test[i] <= test[i+1] for i in range(0, length-1)]))


# heapsort P298


