'''
num=int(input("Enter a number: "))
print(num)



if num>0:
    print("number is positive")

elif num<0:
    print("number is negative")
else:
    print("number is zero")
'''
from re import match
from unittest import case

'''
age=int(input("enter your age:"))

if age>18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
'''

'''
num=int(input("enter a number:"))

if num%2==0:
    print("number is even")
else:
    print("number is odd")

'''

'''
a=int(input("enter a number:"))
match(a):
    case 1:
        print("Sunday")
    case 2:
        print("Monday")
    case 3:
        print("Tuesday")
    case 4:
        print("Wednesday")
    case 5:
        print("Thursday")
    case 6:
        print("Friday")
    case 7:
        print("Saturday")
    case _:
        print("Invalid input")

'''

'''
num1=int(input("enter a number:"))
num2=int(input("enter another number:"))

a=input("enter operation to do:")

match a:
    case "+":
        print(num1+num2)
    case "-":
        print(num1-num2)
    case "*":
        print(num1*num2)
    case "/":
        print(num1/num2)
    case _:
        print("Invalid input")
'''
'''
for i in range(1,11):
    print(i)
'''
'''
num=int(input("enter a number for table: "))
for i in range(1,11):
    print(f"{num}x{i}={num*i}")
'''
'''
sum=0
for i in range(1,101):
    sum+=i
print(sum)
'''
'''
n=int(input("enter a number:"))
for i in range(1,n+1):
    print(i*"*")
*
**
***
****
'''

'''
i=1
sum=0
while i<101:
    sum+=i
    i+=1
print(sum)
'''
'''
password="Aarav@2856"
pasns=""
while pasns!=password:
    pasns=input("enter a password:")
    if pasns==password:
        print("password is correct")
        break
    print("incorrect password")

'''

'''
num=4522
print(int(str(num)[::-1]))
'''
'''
for i in range(1,11):
    if i==7:
        break
    print(i)
'''

'''
for i in range(1,11):
    if i==5:
        continue
    print(i)

'''
'''
for i in range(1,11):
    if i==3:
        pass
    print(i)
'''

