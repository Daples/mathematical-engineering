
def listProduct(*nums):
    s = 1
    for i in nums:
        s *= i
    return s

def smartInsert(data,*nums):
    nums = list(nums)
    try:
        nums.index(data)
    except ValueError:
        nums.append(data)
    print(nums)
