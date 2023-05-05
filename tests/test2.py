import numpy as np
import math

class Point:
    def __init__(self, p, id):
        self.pos = np.array(p)
        self.id = id

a = Point([1,2], 1)
b = Point([10,2], 2)
c = Point([5,5], 3)
d = Point([1,1], 4) # dupe of target

points = [a,b,c,d]

target = np.array([1,1])

closest = sorted(points, key= lambda p: math.dist(p.pos, target))

for i in closest:
    print("point: {}, dist: {}".format(i.pos, math.dist(i.pos, target)))

# closest = [i for i in closest if not np.array_equal(i.pos, target)]

closest = [i for i in closest if i.id != 4]

print("------")

for i in closest:
    print("point: {}, dist: {}".format(i.pos, math.dist(i.pos, target)))

closest = closest[0:2]

print(len(closest))
print(len(points))