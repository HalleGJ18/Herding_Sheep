import numpy as np

arr1 = np.array([10, 71])
arr2 = np.array([3, 20])
# print(arr1 + arr2)
# print((1/2.75645)*arr2)

class clown:
    def __init__(self, s):
        self.size = s

    def check_identity(self, clowns):
        for c in clowns:
            if c == self:
                print("it me")
            else:
                print("not me")

obj1 = clown(2)
obj2 = clown(3)

clowns = [obj1, obj2]

obj1.check_identity(clowns)

testArr = np.array([1,2,None,0])
print(testArr)



