import textwrap
x = str(input("Enter the 100 Bit Data:"))
k = 20
a = 4
A = []
isum = "1111"
arr = [x[i:i+k] for i in range(0, len(x), k)]
for j in range(0, 5):
    y = str(arr[j])
    z = textwrap.wrap(y, a)
    print(z)
    Sum = bin(int(z[0], 2)+int(z[1], 2)+int(z[2], 2)+int(z[3], 2)+int(z[4], 2))[2:]
    if len(Sum) > a:
        X = len(Sum) - a
        Sum = bin(int(Sum[0:X], 2) + int(Sum[X:], 2))[2:]
    if len(Sum) < a:
        Sum = '0' * (a - len(Sum)) + Sum
    iSum = bin(int(isum, 2) - int(Sum, 2))[2:]
    if len(iSum) < a:
        iSum = '0' * (a - len(iSum)) + iSum
    print(Sum)
    print(iSum)
    A.append(iSum)
Check = (''.join(A))
print("Data:"+x)
print("CheckSum:"+Check)
print("Transmitted Data:"+x+Check)