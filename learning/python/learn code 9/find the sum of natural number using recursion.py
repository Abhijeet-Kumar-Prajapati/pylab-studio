def NNS (n):
    if n<=1:
        return n
    else:
        return (n)+NNS(n-1)
n= int(input("enter anumber here:"))
if n<=0:
    print("enter a+ve number")
else:
    print("the sum of natural number upto given rangeis  ",NNS(n))