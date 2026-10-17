# class number:
#     def _init_(self,n):
#         self.n=n
#     def _ add _(self,num):
#         return self.n+num
# n= Number(1)
# m =Number(2)
# print(n+m)




class Number:
    def __init__(self, n):  # Corrected to __init__
        self.n = n

    def __add__(self, other):  # Corrected to __add__
        if isinstance(other, Number):  # Check if 'other' is an instance of Number
            return self.n + other.n
        return NotImplemented  # Return this if addition is not defined for 'other'

# Create instances of Number
n = Number(1)
m = Number(2)

# Use the + operator, which calls __add__
print(n + m)  # Output: 3
