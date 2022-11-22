size = 10
for x in range(size):
    for y in range(4*size+1):
        dist1 = ((x-size)**2 + (y-size)**2) ** 0.5
        dist2 = ((x-size)**2 + (y-3*size)**2) ** 0.5
        if dist1 < size + 0.5 or dist2 < size + 0.5:
            print('V', end=' ')
        else:
            print(' ', end=' ')
    print()

for x in range(1, 2*size):
    for y in range(x):
        print(' ', end=' ')
    for y in range(4*size+1-2*x):
        print('V', end=' ')
    print()


