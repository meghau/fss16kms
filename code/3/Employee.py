class Employee(object):
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return self.__class__.__name__ + self.kv(self.__dict__)
    
    def kv(self, d):
        return '\t'.join(['%s: %s' % (k,d[k]) for k in sorted(d.keys())])
    
    def __lt__(self, other):
        return self.age < other.age

emp1 = Employee('Mark',30)
emp2 = Employee('Allison', 20)
emp3 = Employee('Steve', 45)

emp_list = [emp1, emp2, emp3]

print("Before sorting:")
for e in emp_list:
    print e

print("")
print("After sorting:")
for e in sorted(emp_list):
    print e

