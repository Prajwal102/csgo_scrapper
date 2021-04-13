def mat(matr,sub_size):
    tmp = [(0,0),(0,1),(1,0),(1,1)]
    for i in range(len(matr)-sub_size+1):
        for j in range(len(matr[0])-sub_size+1):
            total = 0
            for a in range(i,i+sub_size):
                for b in range(j,j+sub_size):
                    total += matr[a][b]
            print(total)





matr = [[8,7,6,5],[4,3,2,1],[0,-1,-2,-3],[-4,-5,-6,-7]]

mat(matr,2)

#  8  7     6     5
#  4  3     2     1
#  0  -1    -2      -3
#  -4   -5  -6 -    7