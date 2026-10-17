# class Employee:
#     def _init_(self)
#         print("constructor of Employee")
#     a=1
# class programmer(Employee):
#     def _init_(self):
#       print("constructor of programmer")
#     b=2
# class manager(programmer):
#     def _init_(self):
#         print("constructor of manager")
# O=Employee()
# print(O.a)
# O=programmer()
# print(o.a,o.b)
# O=Manager()
# print(o.a,o.b,o.c)




class Employee:
    def __init__(self):  # Corrected from _init_ to __init__
        print("Constructor of Employee")
    a = 1

class Programmer(Employee):
    def __init__(self):  # Corrected from _init_ to __init__
        super().__init__()  # Call the parent constructor
        print("Constructor of Programmer")
    b = 2

class Manager(Programmer):
    def __init__(self):  # Corrected from _init_ to __init__
        super().__init__()  # Call the parent constructor
        print("Constructor of Manager")
    c = 3

# Create objects and access attributes
O = Employee()
print(O.a)

O = Programmer()
print(O.a, O.b)

O = Manager()
print(O.a, O.b, O.c)
