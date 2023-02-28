import numpy as np

# arr1 = np.array([10, 71])
# arr2 = np.array([3, 20])
# # print(arr1 + arr2)
# # print((1/2.75645)*arr2)

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

clowns = np.array([obj1, obj2])

# obj1.check_identity(clowns)

# testArr = np.array([1,2,None,0])
# print(testArr)

# arr = np.array([100, 150, 72, 0, 102, 97])

arr = np.array([101, 75])
filtered = arr <= 100
print(filtered)
# filtered[3] = False
print(filtered)
new_arr = arr[filtered]
print(new_arr)

filtered_clowns = clowns[filtered]
print(len(filtered_clowns))
print(filtered_clowns[0].size)

a1 = np.array([1,2])
a2 = np.array([10,10])
heading = a1 + a2
print(heading)



