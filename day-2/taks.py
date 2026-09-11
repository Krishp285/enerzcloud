# Practice Exercises
# Write a program that takes two numbers from the user and divides them, handling division by zero and invalid input errors.

a = input("Enter first number: ")
b = input("Enter second number: ")
try:
    num1 = float(a)
    num2 = float(b)
    result = num1 / num2
    print(f"The result of dividing {num1} by {num2} is: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")
except ValueError:
    print("Error: Invalid input. Please enter numeric values.")
# Create a function that reads a file path from the user, attempts to open and print the file content, and handles file not found or permission errors gracefully.
def read_file():
    file_path = input("Enter the file path: ")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except PermissionError:
        print("Error: Permission denied. You do not have access to this file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#  Practice Exercises
# Write a program that asks the user for a filename and some text, writes the text to that file, and then reads it back to display.
def write_and_read_file():
    filename = input("Enter the filename: ")
    text = input("Enter the text to write to the file: ")
    with open(filename, 'w') as file:
        file.write(text)
    print(f"Text written to {filename}. Now reading the file content:")
    with open(filename, 'r') as file:
        content = file.read()
        print(content)


# Create a program to count the number of words in a text file.
def count_words_in_file():
    filename = input("Enter the filename: ")
    try:
        with open(filename, 'r') as file:
            content = file.read()
            word_count = len(content.split())
            print(f"The file '{filename}' contains {word_count} words.")
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")