# class Employee:
#     a=1
#     @classmethod
#     def show(cls):
#         print(f"the class attribute of is {cls.a}")
#     @property
#     def name(self):
#        return self.ename
#     @name.setter 
#     def name (self.value):
#         self.ename= Value.split("")[0]
#         self.fname=value.split(" ")[1]
#     e=Employee()
#     e.a=45
#     e.name="harry"
#     print(e.name)
#     e.show()



class Employee:
    a = 1  # Class attribute

    @classmethod
    def show(cls):
        print(f"The class attribute is {cls.a}")

    @property
    def name(self):
        return self.ename

    @name.setter
    def name(self, value):
        # Split the value into first and last names
        self.ename = value.split(" ")[0]
        self.fname = value.split(" ")[1] if len(value.split(" ")) > 1 else ""

# Create an instance of Employee
e = Employee()

# Modify the instance and class attributes
e.a = 45
e.name = "Harry Potter"

# Print the name property
print(e.name)  # Output: "Harry"

# Call the class method
e.show()
