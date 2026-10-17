# class employee:
#     language ="python"
#     salary=12000000
#     def getInfo():
#         print(f:"the language is {self.language}. the salary is {salary} ")


# harry = employee()
# #harry.language ="javescript"
# #harry.getInfo()
# employee.getInfo(harry)



class Employee:
    language = "python"
    salary = 12000000

    def getInfo(self):  # Add 'self' as a parameter to the method
        print(f"The language is {self.language}. The salary is {self.salary}.")

# Create an instance of Employee
harry = Employee()
harry.language = "javascript"  # Fixed typo from "javescript" to "javascript"

# Call the method correctly
harry.getInfo()  # This works with the instance
# Or
Employee.getInfo(harry) 
harry .greet()
harry.getInfo()
# This works by passing the instance explicitly
