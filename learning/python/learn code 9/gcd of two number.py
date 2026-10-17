# def  findHcf (x,y):
#     if x>y:
#         smaller =y
#     else:
#         smaller =x 
#     for i in range (1, smaller+1):
#         if ((x%i==0)and (y%i==0))
#            hcf =i
#     return hcf
# print ("the hcf of the given two number is ",findHcf(12,30))


#error program

def findHcf(x, y):
    if x > y:
        smaller = y
    else:
        smaller = x
    
    for i in range(1, smaller + 1):
        if (x % i == 0) and (y % i == 0):
            hcf = i
    return hcf

print("The HCF of the given two numbers is", findHcf(12, 30))

