# punc ='''!()-[]}{};:' "\,<>./?@#$%^&*_~'''
# string = input ("enter anything here:")
# empty_str =""
# for  i in string:
#     if i not in punc:
#         empty_ str +=i # empty_str+i
# print (empty_str)



punc = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''
string = input("Enter anything here: ")
empty_str = ""  # Correct variable initialization

for i in string:
    if i not in punc:
        empty_str += i  # Fixed variable name here

print(empty_str)
