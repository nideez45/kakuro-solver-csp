import bs_mac
import input

rows = input.rows
colms = input.colums
answer = bs_mac.answer

output_matrix_vertical = input.matrix_vertical
output_matrix_horizontal = input.matrix_horizonal

# making the output matrix

for i in range(rows):
    for j in range(colms):
        if(output_matrix_vertical[i][j]=='0'):
            output_matrix_vertical[i][j] = answer[(i,j)]
            
for i in range(rows):
    for j in range(colms):
        if(output_matrix_horizontal[i][j]=='0'):
            output_matrix_horizontal[i][j] = answer[(i,j)]

# making output file

with open('output7.txt', 'w') as f:
    f.write("rows={}\n".format(rows))
    f.write("columns={}\n".format(colms))
    f.write("Horizontal\n",)
    for lists in output_matrix_horizontal:
        cnt=0
        for item in lists:
            cnt+=1
            if(cnt==colms):
                f.write("%s" % item)
            else:    
                f.write("%s," % item)
        f.write("\n")
        
    f.write("Vertical\n",)
    for lists in output_matrix_vertical:
        cnt=0
        for item in lists:
            cnt+=1
            if(cnt==colms):
                f.write("%s" % item)
            else:    
                f.write("%s," % item)
        f.write("\n")
