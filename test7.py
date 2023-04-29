# python program to check if a path exists
#if path doesn’t exist we create a new path
import os
try:
   os.makedirs("output")
except FileExistsError:
   # directory already exists
   pass
 
i = 1
num_exists = True
while num_exists:
    n = str(i).zfill(3)
    filename = "/output/data"+n+".csv"
    if os.path.exists(filename):
        i += 1
    else:
        break

print(filename)