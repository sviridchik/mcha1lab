import numpy as np


# data
C = np.array([[0.2, 0, 0.2, 0, 0],
               [0, 0.2, 0, 0.2, 0],
               [0.2, 0, 0.2, 0, 0.2],
               [0, 0.2, 0, 0.2, 0],
               [0, 0, 0.2, 0, 0.2]
               ])

D = np.array([
    [2.33, 0.81, 0.67, 0.92, -0.53],
    [-0.53, 2.33, 0.81, 0.67, 0.92],
    [0.92, -0.53, 2.33, 0.81, 0.67],
    [0.67, 0.92, -0.53, 2.33, 0.81],
    [0.81, 0.67, 0.92, -0.53, 2.33]
])

b = np.array([4.2, 4.2, 4.2, 4.2, 4.2]).reshape(-1, 1)
eps = 0.0001
k = 9
# A = (k * C + D)
#
# Ab = np.concatenate([A, b], axis=1)

def process_data(b,k,C,D):
    A = (k * C + D)

    Ab = np.concatenate([A, b], axis=1)
    return Ab

print(process_data(b,k,C,D))


Abb1 = np.array([[1, -1, -5], [2, 1, -7]])
Abb = np.array([[1,2,-1,9],[2,-1,3,13],[3,2,-5,-1]])

def hause_reversed(Ab):
    n = Ab.shape[0]
    m = Ab.shape[1]
    answers = []
    i = -1
    for nn in range(n-1,-1,-1):
        if i > n-1:
            return answers
        else:
            i+=1
            actions = []
        for mm in range(m-1,m-i-3,-1):
            actions.append(Ab[nn][mm])
        #print(actions)
        l = len(answers)
        for j in range(1,l+1):
            actions[0]-=actions[j]*answers[j-1]
        answers.append(actions[0]/actions[-1])
    print(answers)
    return answers


def hause_straight(Ab, neps = 4 ):
    n = Ab.shape[0]
    m = Ab.shape[1]
    main_value = 0
    #Abb = np.array([[1, 2, -1, 9], [2, -1, 3, 13], [3, 2, -5, -1]])
    #Abb = np.array([[1, -1, -5], [2, 1, -7]])
    for i in range(n):
        main_value = Ab[i][i]
        if main_value == 0:
            print("Impossible")
            return
        # print(main_value)
        tmp = (Ab[i] / main_value).round(neps)
        # print(tmp)
        for j in range(i + 1, n):
            tmp_res = tmp * Ab[j][i] * (-1)
            Ab[j] = tmp_res + Ab[j]
            Ab[j] = Ab[j].round(neps)
    hause_reversed(Ab)
    #print(Abb)
    return Ab

hause_straight(Abb1)






