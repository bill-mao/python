#
# @lc app=leetcode id=56 lang=python3
#
# [56] Merge Intervals
#
# https://leetcode.com/problems/merge-intervals/description/
#
# algorithms
# Medium (34.97%)
# Total Accepted:    313.9K
# Total Submissions: 897.5K
# Testcase Example:  '[[1,3],[2,6],[8,10],[15,18]]'
#
# Given a collection of intervals, merge all overlapping intervals.
# 
# Example 1:
# 
# 
# Input: [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
# Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into
# [1,6].
# 
# 
# Example 2:
# 
# 
# Input: [[1,4],[4,5]]
# Output: [[1,5]]
# Explanation: Intervals [1,4] and [4,5] are considered overlapping.
# 
#
# Definition for an interval.
# class Interval:
#     def __init__(self, s=0, e=0):
#         self.start = s
#         self.end = e

class Solution:
    def merge(self, intervals: List[Interval]) -> List[Interval]:
        # solution1: sort and merge; nlogn
        # solution2: 
        if len(intervals)  < 2: return intervals
        intervals.sort(key = lambda x:x.start)
        ans = []
        def judge(a, b):
            if a.start <= b.start:
                if a.end >= b.end:
                    return Interval(a.start, max(a.end, b.end))
                else: return None
            else:
                if a.start <= b.end:
                    return Interval(b.start, max(a.end, b.end))
                else: return None
        ans.append(intervals[0])
        for cur in intervals[1:]:
            nexti = judge(cur, ans[-1])
            if nexti:
                ans.pop()
                ans.append(nexti)
            else:
                ans.append(cur)
        return ans
        

