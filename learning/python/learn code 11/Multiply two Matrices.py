# A=[[1,2,3],
#    [2,3,4],
#    [2,34,56]]
# B=[[2,4,55,5],
#    [4,56,6,6],
#    [4,5,6,7]]
# result=[[0,0,0,0],
#         [0,0,0,0],
#         [0,0,0,0]]
# for i in range(len(A)):
#     for j in range (len(B[0])):
#         for k in range(len(B)):
#           result[i][j]+=A[i][k]*B[k][j]
# for i in result:
# print(i) 



A = [[1, 2, 3],
     [2, 3, 4],
     [2, 34, 56]]

B = [[2, 4, 55, 5],
     [4, 56, 6, 6],
     [4, 5, 6, 7]]

# Initialize the result matrix with zeros
result = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

# Perform matrix multiplication
for i in range(len(A)):
    for j in range(len(B[0])):
        for k in range(len(B)):
            result[i][j] += A[i][k] * B[k][j]

# Print the result
for i in result:
    print(i)
