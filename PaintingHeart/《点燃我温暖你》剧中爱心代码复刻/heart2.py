
for y in range(9, -6, -1):
    for x in range(-8, 9):
        print('*##*'[(x+10)%4] if (x*x+y*y-25)**3 < 25*x*x*y*y*y else '-', end=' ')
    print()


# for y in range(9, -6, -1):
#     for x in range(-8, 9):
#         print('1' if (x*x+y*y-25)**3 < 25*x*x*y*y*y else ' ', end=' ')
#     print()


