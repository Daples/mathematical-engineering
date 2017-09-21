from DataStructures import LinkedList, ArrayList


def list_product(*nums):
    s = 1
    for i in nums:
        s *= i
    return s


def smart_insert(data, nums):
    try:
        nums.index(data)
    except ValueError:
        nums.append(data)

    return nums

