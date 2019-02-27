
def get_iter():
    for i in range(3):
        for j in range(3):
            yield (i,j)

print(list(get_iter()))


import random

a = [1,2,5,3,4]

print(random.shuffle(a))

print(a)
