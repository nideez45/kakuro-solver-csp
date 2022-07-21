import input

MatrixH = input.matrix_horizonal
MatrixV = input.matrix_vertical
rows = input.rows
colums = input.colums

variables = []

# for vertical matrix

# making column constraints

neighbors = {}
for i in range(rows):
    for j in range(colums):
        if(MatrixV[i][j]!='#'):
            if(MatrixV[i][j] == '0'):
                variables.append((i,j))
            else:
                x,y = i,j
                cnt = 0
                for k in range(i+1,rows):
                    if(MatrixV[k][j] != '0'):
                        break
                    if (i,j) not in neighbors:
                        neighbors[(i,j)] = list()
                    neighbors[(x,y)].append((k,j))

l = list()
values = list()                    
for ele in neighbors:
    l.append(neighbors[ele])
    values.append(int(MatrixV[ele[0]][ele[1]]))
colum_constraint = l
colum_sum = values
    
# for Horizontal matrix

# making row constraints

neighbors = {}
for i in range(rows):
    for j in range(colums):
        if(MatrixH[i][j]!='#'):
            if(MatrixH[i][j] == '0'):
                variables.append((i,j))
            else:
                x,y = i,j
                for k in range(j+1,colums):
                    if(MatrixH[i][k] != '0'):
                        break
                    if (i,j) not in neighbors:
                        neighbors[(i,j)] = list()
                    neighbors[(x,y)].append((i,k))

l = list()
values = list()     
for ele in neighbors:
    l.append(neighbors[ele])
    values.append(int(MatrixH[ele[0]][ele[1]]))
row_constraint = l
row_sum = values

# print(final_variables)
# print(row_constraint)
# print(row_sum)