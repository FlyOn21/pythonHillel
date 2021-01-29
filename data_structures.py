# 1) Write a function def solution(A) that, given an array A of N integers, returns the smallest positive integer (greater than 0) that does not occur in A.
# For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.
# Given A = [1, 2, 3], the function should return 4.
# Given A = [−1, −3], the function should return 1.

def smallest_positive_integer(A=[1, 3, 6, 4, 1, 2]):
    """Function returns the smallest positive integer (greater than 0) that does not occur in A"""
    set_array_A_positiv_value = {unit for unit in set(A) if unit > 0}
    if max(A) < 1:
        pull_search_values = {unit for unit in range(min(A), 2) if unit > 0}
    elif max(A) >= 1:
        pull_search_values = {unit for unit in range(min(A), (max(A) + 1)) if unit > 0}
    if set_array_A_positiv_value != pull_search_values:
        return min(set.symmetric_difference(set_array_A_positiv_value, pull_search_values))
    else:
        return max(pull_search_values) + 1


# 2)Abinary gapwithin a positive integer N is any maximal sequence of consecutive zeros that
# is surrounded by ones at both ends in the binary representation of N.
# For example, number 9 has binary representation1001and contains a binary gap of length 2.
# The number 529 has binary representation 1000010001 and contains two binary gaps: one of
# length 4 and one of length 3. The number 20 has binary representation 10100 and contains one binary gap of length 1.
# The number 15 has binary representation 1111 nd has no binary gaps. The number 32 has binary representation 100000 and has no binary gaps.
# Write a function:
# def solution(N)
# that, given a positive integer N, returns the length of its longest binary gap. The function should return 0 if N doesn't contain a binary gap.
# For example, given N = 1041 the function should return 5, because N has binary representation 10000010001 and so
# its longest binary gap is of length 5. Given N = 32 the function should return 0, because N has binary representation '100000' and thus no binary gaps.
def longest_binary_gap(N=32):
    """Function count binary gap in binary representation integer N"""
    binary_represent_N = bin(N)[2:]
    list_char_binary_represent_N = str(binary_represent_N).strip('0').split('1')
    list_binary_gap = [(len(char)) for char in list_char_binary_represent_N if char != '']
    if list_binary_gap == []:
        return 0
    else:
        return max(list_binary_gap)


# 3)An array A consisting of N integers is given. Rotation of the array means that each element is shifted right by one index,
# and the last element of the array is moved to the first place. For example, the rotation of array A = [3, 8, 9, 7, 6] is [6, 3, 8, 9, 7]
# (elements are shifted right by one index and 6 is moved to the first place).
# The goal is to rotate array A K times; that is, each element of A will be shifted to the right K times.
# Write a function:
# def solution(A, K)
# that, given an array A consisting of N integers and an integer K, returns the array A rotated K times.
# For example, given
#     A = [3, 8, 9, 7, 6]
#     K = 3
# the function should return [9, 7, 6, 3, 8]. Three rotations were made:
#     [3, 8, 9, 7, 6] -> [6, 3, 8, 9, 7]
#     [6, 3, 8, 9, 7] -> [7, 6, 3, 8, 9]
#     [7, 6, 3, 8, 9] -> [9, 7, 6, 3, 8]
# For another example, given
#     A = [0, 0, 0]
#     K = 1
# the function should return [0, 0, 0]
# Given
#     A = [1, 2, 3, 4]
#     K = 4
# the function should return [1, 2, 3, 4]
def rotation_array(A=[3, 8, 9, 7, 6], K=3):
    """Function rotation given array \"K\" times"""
    counter = 0
    while counter < K:
        last_unit_array = A.pop(-1)
        A.insert(0, last_unit_array)
        counter += 1
    return A


if __name__ == '__main__':
    print('Task #1')
    result = smallest_positive_integer()
    print(result)

    print('Task #2')
    result = longest_binary_gap()
    print(result)

    print('Task #3')
    result = rotation_array()
    print(result)
