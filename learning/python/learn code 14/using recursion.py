def fact(a):
    if  a == 0:
        return 1
    else:
        return((a)*fact(a-1))
num = int(input("entera number:"))
result =fact(num) 
print("the factorial of the given number is ",result)