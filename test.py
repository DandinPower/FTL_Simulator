import copy 

class Variable:
    def __init__(self, value) -> None:
        self.value = value 
    
    def __repr__(self):
        return f'{self.value}'

a = []

x = Variable(1)

y = Variable(2)

a.append(x)
a.append(y)

print(a)

b = []

for _a in a:
    b.append(_a)

x.value = 3

print(b)

a[0].value = 4

print(b)