# class Employee:
#     company="ITC"
#     def show (self):
#         print(f"the name of the employee is  {self.name} and the salary is {self.salary}")
# # class programmer:
#     # company="ITC Infotech"
#     # def show(self):
#         # print(f"the name is {self.name} and the salary is {self.salary}")
#     # def show language(self):
#         # print(f"thename is {self.name} and the salary is {self.language} language")
#     class programmer(employee):
#         company="ITC Infotech"
#     def showlanguage(self):
#         print(f"the name is {self .name} and he is good with {self .language} language")
#     a= employee()
#     b=programmer()
#     print(a.company,b.company)




# # same pragram



class Employee:
    company = "ITC"

    def show(self):
        print(f"The name of the employee is {self.name} and the salary is {self.salary}")


class Programmer(Employee):  # Correct inheritance
    company = "ITC Infotech"

    def show_language(self):
        print(f"The name is {self.name} and they are good with {self.language} language")


# Create instances
a = Employee()
a.name = "Alice"  # Dynamically assign the 'name' attribute
a.salary = 50000  # Dynamically assign the 'salary' attribute

b = Programmer()
b.name = "Bob"  # Dynamically assign the 'name' attribute
b.salary = 70000  # Dynamically assign the 'salary' attribute
b.language = "Python"  # Dynamically assign the 'language' attribute

# Print company names
print(a.company)  # Output: ITC
print(b.company)  # Output: ITC Infotech

# Call methods
a.show()
b.show()
b.show_language()
