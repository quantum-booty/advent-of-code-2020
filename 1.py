import numpy as np
##
x = [1721, 979, 366, 299, 675, 1456]

# x = np.loadtxt('inputs/1.txt')

with open('inputs/1.txt') as f:
    x = [int(line.strip()) for line in f]

# O(n^3)
n = len(x)
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            a = x[i]
            b = x[j]
            c = x[k]
            sum = a + b + c
            if sum == 2020:
                # print(a, b, c)
                print(a * b * c)

##
from typing import List

INPUTS = [1721, 979, 366, 299, 675, 1456]


def find_product(inputs: List[int]) -> int:
    # O(n)
    needs = {2020 - i for i in inputs}

    num = 0
    # O(n)*O(1) = O(n)
    # overall O(n)
    for i in inputs:
        if i in needs:
            num = i
            break

    return num * (2020 - num)


assert find_product(INPUTS) == 514579


def find_product3(inputs: List[int]) -> int:
    # dictionary comprehension O(n^2)
    needs = {2020 - i - j: (i, j) for i in inputs for j in inputs if i != j}
    # for loop with dictionary look up: O(n)*O(1) = O(n)
    # overall time complexity O(n^2)
    for i in inputs:
        if i in needs:
            j, k = needs[i]
            return i * j * k


assert find_product3(INPUTS) == 241861950

with open('inputs/1.txt') as f:
    x = [int(line.strip()) for line in f]
    print(find_product3(x))
