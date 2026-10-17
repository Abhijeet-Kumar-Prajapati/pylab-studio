# from functools import reduce
# # map example
# l=[1,2,3,4,5]
# square=lambda x:x*x
# sqlist = map(square,l)
# print(list(sqlist))
# # filter example
# def even (n):
#     if (n%2==0):
#         return True
#     return False
# onlyEven=filter(even,l)
# print(list(onlyEven))
# # reduce example
# def sum(a,b):
#     return a+b
# mul= lambda x,y:x*y
# print(reduce(l))
# print(reduce(mul,l))



from functools import reduce

# map example
l = [1, 2, 3, 4, 5]
square = lambda x: x * x
sqlist = map(square, l)
print(list(sqlist))  # Output: [1, 4, 9, 16, 25]

# filter example
def even(n):
    return n % 2 == 0

onlyEven = filter(even, l)
print(list(onlyEven))  # Output: [2, 4]

# reduce example
def sum(a, b):
    return a + b

mul = lambda x, y: x * y

# Using reduce to find the sum of elements
print(reduce(sum, l))  # Output: 15

# Using reduce to find the product of elements
print(reduce(mul, l))  # Output: 120
