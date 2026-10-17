# a= "harry potter and the prisoner of Azkaban"
# vowels="aeiou"
# A=A. casefold ()
# print(A)
# count= {}.fromkeys(vowels,0)
# for char in A:
#     if char in count:
#         count[char]+=1
# print(count)



a = "harry potter and the prisoner of Azkaban"
vowels = "aeiou"
a = a.casefold()  # Use lowercase consistently for comparison
print(a)
count = {}.fromkeys(vowels, 0)  # Initialize a dictionary with vowels as keys and 0 as initial values

for char in a:
    if char in count:
        count[char] += 1

print(count)
