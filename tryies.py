import numpy as np
a = np.array([[1,2],
             [3,4],
              [9,11]])
print(a)
a[[0,2]] = a[[2,0]]
print(a)