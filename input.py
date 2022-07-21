import re

with open('puzzles/input7.txt') as f:
    lines = f.readlines()
    
# reading input    
    
    
temp = re.findall(r'\d+', lines[0])
res = list(map(int, temp))
rows = int(res[0])

temp = re.findall(r'\d+', lines[1])
res = list(map(int, temp))
colums = int(res[0])

# getting horizontal matrix

matrix_horizonal = []
for j in range(rows):
    l = []
    s = ""
    for i in range(len(lines[j+3])):
        if(lines[j+3][i] == '\n'):
            l.append(s)
            s = ""
        elif(lines[j+3][i]) == ',':
            l.append(s)
            s = ""
        else:
            s = s + lines[j+3][i]

    matrix_horizonal.append(l)
    
#print(matrix_horizonal)

# getting vertical matrix

matrix_vertical = []
for j in range(rows):
    l = []
    s = ""
    for i in range(len(lines[j+rows+4])):
        if(lines[j+rows+4][i] == '\n'):
            l.append(s)
            s = ""
        elif(lines[j+rows+4][i]) == ',':
            l.append(s)
            s = ""
        else:
            s = s + lines[j+rows+4][i]
    
    if(s!=""):
        l.append(s)
            
    matrix_vertical.append(l)
    
# print(matrix_vertical)
