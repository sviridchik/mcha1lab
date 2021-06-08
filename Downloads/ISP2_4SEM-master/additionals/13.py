# https://www.youtube.com/watch?v=Xgaj0Vxz_to&ab_channel=%D0%A4%D0%BE%D0%BA%D1%81%D1%84%D0%BE%D1%80%D0%B4
# https://foxford.ru/wiki/informatika/bystraya-sortirovka-hoara-python

# quick
import random as ra


def Quck_sort(data):
    if len(data) <= 1:
        return data
    else:
        pivot = ra.choice(data)
        l = []
        r = []
        m = []
        for elem in data:
            if elem < pivot:
                l.append(elem)
            elif elem > pivot:
                r.append(elem)
            else:
                m.append(elem)
    return Quck_sort(l) + m + Quck_sort(r)


# merge  https://foxford.ru/wiki/informatika/sortirovka-sliyaniem?provider=google_oauth2
def merge(a, b):
    res = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res += a[i:] + b[j:]
    return res


def merge_sort(data):
    if len(data) <= 1:
        return data
    else:
        l = data[:len(data) // 2]
        r = data[len(data) // 2:]
    return merge(merge_sort(l), merge_sort(r))

# regex

def regex_sort(a):
    length = len(str(max(a)))
    rang = 10

    for i in range(length):
        b = [[] for k in range(rang)]
        for elem in a:
            sign = elem//10**i%10
            b[sign].append(elem)
        a = []
        for k in range(rang):
            a +=b[k]
    print(a)






A = [12, 5, 664, 63, 5, 73, 93, 127, 432, 64, 34]
regex_sort(A)
a = [2, 3, -4, 3, -7, -8, 9]
# print(merge_sort(a))
# https://foxford.ru/wiki/informatika/porazryadnaya-sortirovka