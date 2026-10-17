# class Employee:
#     language = "python"
#     salary = 12000000
  
#     def_ init_(self,name,salary,language):
#     self.name=Name
#     self.salary=salary
#     self.language=language
#        print("i am creating an object")
#     def getInfo(self):  # Add 'self' as a parameter to the method
#         print(f"The language is {self.language}. The salary is {self.salary}.")
#     @staticmethod
#     def greet():
#         print("good morning")
# # Create an instance of Employee
# harry = Employee("harry",13000000,"javascript")
# #harry.name "harry"
# print(harry.name,harry.salary,harry.language)

# #rohan=Employee()


# same program


class Employee:
    language = "python"
    salary = 12000000

    def __init__(self, name, salary, language):  # Correct constructor definition
        self.name = name  # Correct attribute assignment
        self.salary = salary
        self.language = language
        print("I am creating an object")

    def getInfo(self):  # Proper method definition with 'self'
        print(f"The language is {self.language}. The salary is {self.salary}.")

    @staticmethod
    def greet():
        print("Good morning")

# Create an instance of Employee
harry = Employee("harry", 13000000, "javascript")
# Display the attributes of the instance
print(harry.name, harry.salary, harry.language)

# Call a method
harry.getInfo()

# Call the static method
Employee.greet()

# Create another instance
rohan = Employee("rohan", 10000000, "java")
print(rohan.name, rohan.salary, rohan.language)
