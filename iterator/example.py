
def get_iter():
    for i in range(3):
        for j in range(3):
            yield (i,j)

print(list(get_iter()))
