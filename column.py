import numpy as np
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
            actions.append(Abb[nn][mm])
        #print(actions)
        l = len(answers)
        for j in range(1,l+1):
            actions[0]-=actions[j]*answers[j-1]
        answers.append((actions[0]/actions[-1]).round(4))
    print(answers)
    return answers

def hause_straight(Ab, neps = 4 ):
    n = Ab.shape[0]
    m = Ab.shape[1]
    main_value = 0
    #Abb = np.array([[1, 2, -1, 9], [2, -1, 3, 13], [3, 2, -5, -1]])
    #Abb = np.array([[1, -1, -5], [2, 1, -7]])
    for i in range(n):
        Ab = choose_column(Ab,i)
        main_value = Ab[i][i]
        if main_value == 0:
            print("Impossible")
            return
        # print(main_value)
        #tmp = (Abb[i] / main_value).round(neps)
        tmp = Ab[i]
        # print(tmp)
        for j in range(i + 1, n):
            q = (Ab[j][i]/main_value)*(-1)
            tmp_res = tmp * q
            Ab[j] = tmp_res + Ab[j]
            Ab[j] = Ab[j].round(neps)
    #print(Abb)
    return Ab

A = np.array([[3.,4.,-9.,5.,-14.],
          [-15.,-12.,50.,-16.,44.],
          [-27.,-36., 73.,8.,142.],
          [9.,12.,-10.,-16.,-76.]
          ])
def choose_column(A,start_pos):
    m=A[start_pos][start_pos]
    change_index=start_pos
    # for ii in range(A.shape[0]):
    #     choose = []
    for jj in range(start_pos,A.shape[1]-1):
        tmp =  abs(A[jj][start_pos])
        if tmp>m:
            tmp,m =m,tmp
            change_index=jj
    print(m,change_index)
    A[[start_pos,change_index]] = A[[change_index,start_pos]]
    return A

hause_reversed(hause_straight(A))
