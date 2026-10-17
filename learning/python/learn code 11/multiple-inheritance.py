# class Employee:
#     company="ITC"
#     name= "default name"
#     def show(self):
#         print(f"the name of the Employee is {self.name} and the salary is {self.salary}   ")
# class coder:
#     language="python"
#     def printlanguages(self):
#         print(f"out of all the languges here is your language:{self.language}")

# class programmer (employee,coder):
#     company= "ITC Infotech"
#     def showlanguage(self):
#         print(f"the name is {self.company}and he is good with{self.language} language")

# a=Employee()
# b=programmer()
# b.show()
# b.printlanguages()
# b.showlanguage()





class Employee:
    company = "ITC"
    name = "default name"
    salary = 0  # Added a default salary attribute
    
    def show(self):
        print(f"The name of the Employee is {self.name} and the salary is {self.salary}.")

class Coder:
    language = "Python"
    
    def print_languages(self):
        print(f"Out of all the languages, here is your language: {self.language}.")

class Programmer(Employee, Coder):  # Corrected inheritance
    company = "ITC Infotech"
    
    def show_language(self):
        print(f"The company is {self.company} and they are good with {self.language} language.")

# Create objects and demonstrate functionality
a = Employee()
b = Programmer()

b.name = "John Doe"  # Set a name for the programmer
b.salary = 75000  # Set a salary for the programmer

b.show()  # Call the method from Employee class
b.print_languages()  # Call the method from Coder class
b.show_language()  # Call the method from Programmer class
