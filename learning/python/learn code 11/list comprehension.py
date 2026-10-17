# A =[[1,2,4]
#     [4,5,6]]
# T =[[A[j][i] for j in range (len (A))] for i in range (len (A[0]))]
 
#  for i in T:
#        print (i)

A = [[1, 2, 4],
     [4, 5, 6]]

# Transpose of A
T = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

# Print the transposed matrix
for i in T:
    print(i)
