# def fact(n):
#     if n==1:
#         return 1
# else:
#     return (n* fact(n-1))
# n =int (input("enter a number here:") )
# if n<=0:
#     print('factorial of number less than 1 does not exists')
# else:
#     print("factorial of given number is ", fact(n))



def fact(n):
    if n == 1 or n == 0:  # Including 0! = 1 as a standard factorial definition
        return 1
    else:
        return n * fact(n - 1)

n = int(input("Enter a number here: "))
if n < 0:  # Factorial for negative numbers is undefined
    print("Factorial of a number less than 0 does not exist.")
else:
    print("Factorial of the given number is", fact(n))
