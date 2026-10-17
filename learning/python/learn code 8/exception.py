# try:
#     a= int(input("hey,enter a number:"))
#     print(a)
# except valueError as v:
#     print("heyy")
#     print(v)
# except Exception as e:
#     print(e)
# a=int(input ("hey, enter a number:"))
# print("thank you")




try:
    a = int(input("Hey, enter a number: "))
    print(a)
except ValueError as v:
    print("Heyy, that’s not a valid number!")
    print(v)
except Exception as e:
    print("An unexpected error occurred:")
    print(e)

a = int(input("Hey, enter a number again: "))
print("Thank you!")
