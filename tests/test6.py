# arr = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# print(arr[:20])

def check_success(p):
    target = [25,25]
    target_range = 10
    if (p[0] >= target[0]-target_range) and (p[0] <= target[0]+target_range):
        if (p[1] >= target[1]-target_range) and (p[1] <= target[1]+target_range):
            return True 
    return False

print(check_success([14,14])) #f
print(check_success([14,15])) #f
print(check_success([15,14])) #f
print(check_success([15,15])) #t
print(check_success([15,16])) #t
print(check_success([16,15])) #t
print(check_success([20,20])) #t
print(check_success([25,25])) #t
print(check_success([35,34])) #t
print(check_success([34,35])) #t 
print(check_success([35,35])) #t
print(check_success([36,35])) #f
print(check_success([35,36])) #f
print(check_success([36,36])) #f


