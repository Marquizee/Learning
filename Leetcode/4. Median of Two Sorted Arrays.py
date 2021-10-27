# Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
# The overall run time complexity should be O(log (m+n)).

# Example 1:
# Input: nums1 = [1,3], nums2 = [2]
# Output: 2.00000
# Explanation: merged array = [1,2,3] and median is 2.

# Example 2:
# Input: nums1 = [1,2], nums2 = [3,4]
# Output: 2.50000
# Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

# Example 3:
# # Input: nums1 = [0,0], nums2 = [0,0]
# Output: 0.00000

# Example 4:
# Input: nums1 = [], nums2 = [1]
# Output: 1.00000

# Example 5:
# Input: nums1 = [2], nums2 = []
# Output: 2.00000


# Constraints:
# nums1.length == m
# nums2.length == n
# 0 <= m <= 1000
# 0 <= n <= 1000
# 1 <= m + n <= 2000
# -106 <= nums1[i], nums2[i] <= 106

def find_median_sorted_arrays(nums1, nums2):
    array = sorted(nums1 + nums2)
    array_length = len(array)
    if array_length % 2 == 1:
        return array[array_length//2]
    prev = array[(array_length//2)-1]
    curr = array[array_length//2]
    if prev == curr:
        return prev
    return (prev+curr)/2
