from typing import List


def get_same_numbers(List_1: List[int], List_2: List[int]) -> List[int]:
    common = list(set(List_1).intersection(set(List_2)))
    return common

print(get_same_numbers([2,4,6,75,3,5,77,5], [2,7754,43456,6433,23,3,4,55,6,77,8,8]))


def get_same_numbers2(List_1: List[int], List_2: List[int]) -> List[int]:
    common = [x for x in List_1 if x in List_2]
    return common

print(get_same_numbers2([2,4,6,75,3,5,77,5], [2,7754,43456,6433,23,3,4,55,6,77,8,8]))


def get_same_numbers3(List_1: List[int], List_2: List[int]) -> List[int]:
    common = list(filter(lambda x: x in List_1, List_2))
    return common


print(get_same_numbers3([2,4,6,75,3,5,77,5], [2,7754,43456,6433,23,3,4,55,6,77,8,8]))