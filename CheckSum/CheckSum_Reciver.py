import textwrap
x = str(input("Enter the 100 Bit Data:"))
k = 20
a = 4
A = []
R = x[100:120]
i_sum = "1111"
arr = [x[i:i+k] for i in range(0, len(x), k)]
for j in range(0, 5):
    y = str(arr[j])
    z = textwrap.wrap(y, a)
    Sum = bin(int(z[0], 2)+int(z[1], 2)+int(z[2], 2)+int(z[3], 2)+int(z[4], 2))[2:]
    if len(Sum) > a:
        X = len(Sum) - a
        Sum = bin(int(Sum[0:X], 2) + int(Sum[X:], 2))[2:]
    if len(Sum) < a:
        Sum = '0' * (a - len(Sum)) + Sum
    S = R[j*a:(j+1)*a]
    check = bin(int(Sum, 2) + int(S, 2))[2:]
    if len(check) > a:
        X = len(check) - a
        Sum = bin(int(check[0:X], 2) + int(check[X:], 2))[2:]
    iSum = bin(int(i_sum, 2) - int(check, 2))[2:]
    if len(iSum) < a:
        iSum = '0' * (a - len(iSum)) + iSum
    if iSum == "0000":
        print("No Error Detected in "+str(j+1)+" segment")
    else:
        print("Error Detected in "+str(j+1)+" segment and  "+str(j+1)+" segment is discarded")