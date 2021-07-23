
# Inherit class
class Parent:

    weight = 70

    def __init__(self, first, last, height):
        self.first = first                                  # initialize the instance's attributes
        self.last = last
        self.height = height

    def fullname(self):
        return f"{self.first} {self.last}"

    def body_mass_index(self):
        return self.weight / (self.height * self.height)


class Child(Parent):                                        # copy/inherit class Parent to class Child
    pass                                                    # pass: nothing added or changed


child_1 = Child("Max", "Mustermann", 1.80)
child_2 = Parent("Max", "Mustermann", 1.80)

print(child_1.weight)
print(child_1.fullname())
print(child_1.body_mass_index(), child_2.body_mass_index())
print(child_1.body_mass_index() == child_2.body_mass_index())

print("-------------------------")
# ---------------------------------------------------------------------------


# Change var and add functions in subclasses
class Employee:

    min_salary = 5000

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = f"{first}.{last}@email.com"

    def fullname(self):
        return f"{self.first} {self.last}"


class Developer(Employee):                                  # inherit class Employee to class Developer
    min_salary = 5000 + 1000                                # changing 'min_salary' var


class Manager(Employee):
    min_salary = 5000 + 2000

    def __init__(self, first, last, employees=None):        # init function with new parameter 'employees' (None as default)
        super().__init__(first, last)                       # super() makes that class Employee handles these vars which are given in the parameters

        if employees is None:
            self.employees = []                             # 'employees' is the new attr
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print("-->", emp.fullname())


emp_1 = Employee("Felix", "Laden")
print(emp_1.min_salary)

dev_1 = Developer("Max", "Müller")
dev_2 = Developer("Hannah", "Scherz")
print(dev_1.min_salary)

mgr_1 = Manager("Erich", "Heinz")
mgr_2 = Manager("Julia", "Washington", [dev_1, dev_2])

mgr_1.add_emp(dev_1)
mgr_1.print_emps()
print("*")

mgr_2.print_emps()
print("*")
mgr_2.remove_emp(dev_1)
mgr_2.print_emps()

print("-------------------------")
# ---------------------------------------------------------------------------


# Difference between isinstance() and issubclass()

# isinstance(): tells if something (an object) is an instance of a class.
"""
class MyClass:                      # MyClass is a class
    data = 1

mc = MyClass()                      # mc is an instance of class MyClass

"""

print(isinstance(mgr_1, Manager))                           # True, because it's an instance of class Manager
print(isinstance(mgr_1, Employee))                          # True, because Manager inherit from Employee
print(isinstance(mgr_1, Developer))                         # False, because Manager does not inherit from Developer but from Employee
print("*")


# issubclass(): tells if a class is a subclass of another class
"""
class MyClass:                      # MyClass is a class
    data = 1
    
class MyClass2(MyClass):            # MyClass is a subclass of MyClass
    pass

mc = MyClass2()
"""

print(issubclass(Developer, Employee))                      # True, because Developer is a subclass of Employee
print(issubclass(Manager, Employee))                        # True, because Manager is a subclass of Employee
print(issubclass(Manager, Developer))                       # False, because Manager is not a subclass of Developer but of Employee
print("-------------------------")
