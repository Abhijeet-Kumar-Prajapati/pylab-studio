# class Employee:
#     a=1
# class programmer(Employee):
#         b=2
# class manager(programmer):
#       c=3
# O= Employee
# print(O.b)
# O=programmer
# print(O.a,o.b)
# O= manager()
# print(O.A,O.B,O.C)


class Employee:
    a = 1

class Programmer(Employee):
    b = 2

class Manager(Programmer):
    c = 3

# Accessing class attributes
O = Employee
try:
    print(O.b)  # Employee class does not have attribute 'b'
except AttributeError:
    print("AttributeError: 'Employee' object has no attribute 'b'")

O = Programmer
print(O.a, O.b)  # Accessing 'a' from Employee and 'b' from Programmer

O = Manager()  # Creating an instance of Manager
print(O.a, O.b, O.c)  # Accessing attributes from all parent classes
