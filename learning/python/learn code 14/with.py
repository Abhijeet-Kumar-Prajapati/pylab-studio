# f= open ("file .txt")
# print (f.read())
# f.close()
# #the same can be written using with satement like this :
# with open ("file .txt") as f:
#     print(f.read())

# Using the traditional method
f = open("file.txt")
print(f.read())
f.close()

# Using the 'with' statement
with open("file.txt") as f:
    print(f.read())
