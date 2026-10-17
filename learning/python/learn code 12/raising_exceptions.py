# a=(input("enter a number:"))
# b=int(input("entersecond number:"))
# if(b==0):
#     rasie ZeroDivisionError ("hey our program is not meat to divide numbers by zero")
# else:
# print(f"the division a/b is {a/b}")


a = int(input("Enter a number: "))
b = int(input("Enter the second number: "))

if b == 0:
    raise ZeroDivisionError("Hey, our program is not meant to divide numbers by zero.")
else:
    print(f"The division a/b is {a / b}")
