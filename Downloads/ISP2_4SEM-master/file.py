from services import fabric
# import json as js

CONST = 6
def ya_func(x):
    x += CONST
    return x

kaka = fabric.fabrica('pickle')

kaka.dump(ya_func, 'fp')
res = kaka.load('fp')

print(res)
print(res(10))

