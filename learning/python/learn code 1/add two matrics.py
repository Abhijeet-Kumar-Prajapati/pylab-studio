# A =[[1,1,1],
#     [2,2,3,],
#     [3,,34,4]]
# B =[[2,,3,4,]
#     [4,5,6]
#     [5,6,7]]
# result = [[0,0,0],
#           [0,0,0],
#           [0,0,0]]
# for i in range(len(A)):
#     for j in range (len (A[0])):
#         result[i][j]=A[i][j]+B[i][j]
# for r in result:
# print(r)



A = [[1, 1, 1],
     [2, 2, 3],
     [3, 34, 4]]

B = [[2, 3, 4],
     [4, 5, 6],
     [5, 6, 7]]

# Initialize result matrix with the same dimensions as A and B
result = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

# Perform element-wise addition of matrices A and B
for i in range(len(A)):
    for j in range(len(A[0])):
        result[i][j] = A[i][j] + B[i][j]

# Print the result matrix
for r in result:
    print(r)
