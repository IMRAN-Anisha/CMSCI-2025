#exercise 1: shopping cart calculator
prices = [] #defining an array to store the prices

numElements = int(input("enter the number of prices:")) 
for i in range(numElements):
    prices.append

#exercise 2: binary search
def binary_search(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2

        if sorted_list[mid] == target:
            return mid  # Target found, return index
        elif sorted_list[mid] < target:
            low = mid + 1  # Search right half
        else:
            high = mid - 1  # Search left half

    return -1  # Target not found

# Main Program
numbers = input("Enter a sorted list of numbers (comma-separated): ").strip()
sorted_list = list(map(int, numbers.split(",")))
target = int(input("Enter the target number to search: "))

result = binary_search(sorted_list, target)

if result != -1:
    print(f"Target found at index {result}")
else:
    print("Target not found in the list")
