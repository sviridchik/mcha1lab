# theory : https://www.severcart.ru/blog/all/understanding_yield_in_Python/


def Fibb(amount:int):
    "Fibonachi sequence"
    f1, f2 = 0, 1
    for i in range(amount):
        f1, f2 = f2, f1 + f2
        yield f1

print(list(Fibb(15)))
