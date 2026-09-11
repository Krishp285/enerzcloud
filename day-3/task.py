# Practice Exercises
import numpy as np
# Exercise 1: Creating and Manipulating Arrays
# Create a 1D array with elements 10 to 50 (inclusive).
arr1 = np.arange(10, 51)

# Extract elements from index 5 to 15.
arr2 = arr1[5:16]

# Reverse the array.
arr3 = arr1[::-1]

# Print every 3rd element.
arr4 = arr1[::3]

# Exercise 2: 2D Array Indexing
# Create a 3×3 matrix with values 1 to 9.
arr5 = np.arange(1, 10).reshape(3, 3)

# Extract the second row.
arr6 = arr5[1, :]

# Extract the first column.
arr7 = arr5[:, 0]

# Extract a 2×2 submatrix from the top-left corner.
arr8 = arr5[:2, :2]

# Exercise 3: Arithmetic Operations
# Create two arrays: [1, 2, 3] and [4, 5, 6].
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
# Add, subtract, multiply, and divide them.
arr3 = arr1 + arr2
arr4 = arr1 - arr2
arr5 = arr1 * arr2
arr6 = arr1 / arr2
print("Addition:", arr3)
print("Subtraction:", arr4)
print("Multiplication:", arr5)
print("Division:", arr6)
