
def dec(func):
    def wrapper(a):
        print("look what i have ",a)
        print("before")
        func(a)
        print("after")
    return wrapper

@dec
def stand_alone_function(a):
    print("Я простая одинокая функция, ты ведь не посмеешь меня изменять?  ", a)

storage = {}

def cashed(func):
    def wrapper(a1):
        global storage
        if a1 not in storage:
            ans = func(a1)
            storage[a1] = ans
            return ("The ans was calculated by the func . The res is {}".format(ans))
        else:
            return ("The ans was taken  from cashe . The res is {}".format(storage[a1]))

    return wrapper

@cashed
def cubes(n:int)->list:
    res = []
    for i in range(n):
        res.append(i**3)
    return res
print(cubes(5))
print(cubes(5))
print("dfvd")