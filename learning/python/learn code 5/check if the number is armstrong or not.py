num = int(input("Enter a number here: "))
order = len(str(num))  # Calculate the number of digits
sum = 0
temp = num

while temp > 0:
    digit = temp % 10  # Get the last digit
     # cube=digit**3
   #  sum=sum+cube
   #sum+=digit**3
    sum += digit ** order  # Add the digit raised to the power of the order
    temp //= 10  # Remove the last digit

if sum == num:
    print("It is an Armstrong number")
else:
    print("It is not an Armstrong number")