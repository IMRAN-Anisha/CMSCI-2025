print("Hello, World!")

'''
1. a variable is a container for a value
2. data types: int, float, string, boolean, array, dictionary
3. type casting: converting one data type to another
4. integer,float,string,boolean,array
'''
#exercise 1
name = "Anisha"
age = 17
height = 165.1
print("My name is " + name + " I am " + str(age) + " years old and I am " + str(height) + " cm tall")

#exercise 2
num_str = "100"
pi_value = 3.15159

number1 = int(num_str) + 50
number2 = int(pi_value)
print(number1,number2)

#exercise 3
num1 = input("Enter a number: ")
num2 = input("Enter another number: ")
operation = input("Enter an operation: ")
if operation == "+":
    print(int(num1) + int(num2))
elif operation == "-":
    print(int(num1) - int(num2))
elif operation == "*":
    print(int(num1) * int(num2))
elif operation == "/":
    print(int(num1) / int(num2))
    if num2 == 0:
        print("Cannot divide by 0") 

#exercise 4
number = 25
double = number * 2
print("Double of number is " + str(double))    

'''
exercise 5: Why is an understanding of data types important in programming?
Data types are important because they tell the computer how to store and manipulate data.
'''

'''
worksheet 2:
1. X is greater and even
2. error was the logic in the temperatures. over 20 should be comfortable and over 25 should be warm.
'''

temp = 30

if temp > 35:
    print("too hot")
elif temp > 25:
    print("comfortable")
elif temp > 20:
    print("warm")
else:
    print("cold")

#exercise 1: grade evaluator
mark = 60
if mark >= 85:
    grade = "A"
elif 70 <= mark <= 84:
    grade = "B"
elif 55 <= mark <= 69:
    grade = "C"
elif 40 <= mark <= 54:
    grade = "D"
elif 0 < mark < 40:
    grade = "E"
else:
    print("invalid input, enter something between 0-100")

#exercise 2: triangle classifier
lengthOne = int(input)
lengthTwo = int(input)
lengthThree = int(input)

if lengthOne <= 0:
    print("enter a valid number")
if lengthTwo <= 0:
    print("enter a valid number")
if lengthThree <= 0:
    print("enter a valid number")

if lengthOne == lengthTwo == lengthThree:
    print("triangle is equilateral")
if lengthOne == lengthTwo or lengthTwo == lengthThree or lengthOne == lengthThree:
    print("triangle is isosceles")
else:
    print("triangle is scalene")
# making sure the triangle is valid
if lengthOne + lengthTwo > lengthThree and lengthTwo + lengthThree > lengthOne and lengthOne + lengthThree > lengthTwo:
    print("triangle is valid")
else:
    print("triangle is invalid")

#exercise 3: discount calculator
price = int(input)

if price < 50:
    print("no discount applied")
elif 50 <= price <= 99:
    print("discounted price is:", price*0.95)
elif 100 <= price <= 199:
    print("discounted price is:", price*0.9)
elif price >= 200:
    print("discounted price is:", price*0.85)

#exercise 4: leap year checker
year = int(input)  
if year % 4 == 0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("leap year")
        else:
            print("not a leap year")
    else:
        print("leap year")


