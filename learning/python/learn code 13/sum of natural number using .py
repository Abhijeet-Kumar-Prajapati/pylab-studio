# num=int(input ('enter a number here'))
# if num<0:
#     print('please enter +ve no')
# else:
#     sum =0
#     while num>0:
#         sum+=num
#         num-=1
#         print(sum)

 #same program
num = int(input("Enter a number here: "))
if num < 0:
    print("Please enter a positive number")
else:
    sum = 0
    while num > 0:
        sum += num  # Add the current number to the sum
        num -= 1  # Decrement the number by 1
    print("The sum is:", sum)  # Print the final sum