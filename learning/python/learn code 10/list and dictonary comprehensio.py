# A= "harry pottter and the prisoner of azkaban"
# vowels="aeiou"
# A=A.casefold()
# count={key:sum([1 for char in a if char == key])for key in vowels}
# print(count)



A = "harry pottter and the prisoner of azkaban"
vowels = "aeiou"
A = A.casefold()  # Convert the string to lowercase
count = {key: sum([1 for char in A if char == key]) for key in vowels}  # Use A instead of a
print(count)
