#Greet User Function
def greet(name):
    return f"hello, {name}!"

print(greet("krish"))

#Print Even Numbers from List
l = [10,20,1,3,5,6,7,8,9]
for x in l:
    if x%2 == 0:
        print(x)

#Student Data Dictionary
s = {
    "name": "krish",
    "age": 20,
    "course": "python"
}
print(s)

#Calculator with Functions
def add(a,b):
    return a+b
def subtract(a,b):
    return a-b  
def multiply(a,b):
    return a*b
def divide(a,b):
    if b != 0:
        return a/b
    else:
        return "Cannot divide by zero"
choice = input("Enter operation (add, subtract, multiply, divide): ")
match(choice):
    case "add":
        print(add(10, 5))
    case "subtract":
        print(subtract(10, 5))
    case "multiply":
        print(multiply(10, 5))
    case "divide":
        print(divide(10, 5))
    case _:
        print("Invalid operation")


#Mini Quiz
# What is the difference between a list and a dictionary?
# ans :- list is ordered , mutable having heterogeneous elements 
#    dictionary is unordered , mutable having key-value pairs   
# How do you define and call a function in Python?
# ans :- def function_name(parameters):
#         # function body
#         return value (if needed)
#       function_name(arguments)

# What is the output of print("2" + "3")?
# ans :- 23