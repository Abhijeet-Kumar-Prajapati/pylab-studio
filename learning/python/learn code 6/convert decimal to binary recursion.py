# def CovertBinary(n):
#     if n>1:
#         CovertBinary(n//2)
#     print(n%2,end="")
# print("the binary of the given number is :")
# ConvertBinary(15)



def ConvertBinary(n):  # Corrected the function name from "CovertBinary" to "ConvertBinary"
    if n > 1:
        ConvertBinary(n // 2)
    print(n % 2, end="")

print("The binary of the given number is:")
ConvertBinary(32)  # Corrected the function name
