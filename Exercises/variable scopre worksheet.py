#1. python function to compute the factorial of a non negative number
'''
maintain a global counter that tracks how many multiplication  operations are peroformed during calculation
'''
# Global variable to store the sum
total = 0  

def calculate_sum(numbers):
    """Calculates the sum of a list using a global variable."""
    global total
    total = 0  # Reset total before summing
    for number in numbers:
        total += number  # Add each number to the total
    return total

def calculate_average(numbers):
    """Calculates the average by calling calculate_sum() first."""
    if len(numbers) == 0:
        return 0  # Avoid division by zero
    calculate_sum(numbers)  # Ensure total is updated
    return total / len(numbers)  # Compute average

# Main Program
numbers = []  # List to store user inputs

while True:
    user_input = input("Enter a number (or type 'end' to finish): ")
    if user_input.lower() == "end":  # Check for termination condition
        break
    try:
        numbers.append(int(user_input))  # Convert input to integer and store
    except ValueError:
        print("Invalid input. Please enter a number.")

# Compute and display results
if numbers:
    sum_result = calculate_sum(numbers)
    avg_result = calculate_average(numbers)
    print(f"Sum: {sum_result}")
    print(f"Average: {avg_result}")
else:
    print("No numbers entered.")


#2. Average Calculator with global sum variable
'''
module with two functions:
- calculate the sum of a list of numbers using global variable
- compute the average using that sum
'''
# Global inventory list
inventory = []

def add_item(item):
    """Adds an item to the inventory."""
    global inventory
    inventory.append(item)

def remove_item(item):
    """Removes an item if it exists, else prints an error message."""
    global inventory
    if item in inventory:
        inventory.remove(item)
    else:
        print(f"Error: '{item}' not found in inventory.")

def display_inventory():
    """Displays the current inventory."""
    print("Current Inventory:", inventory)

# Main Program
while True:
    command = input("Enter command (add/remove/display/exit): ").strip().lower()

    if command == "add":
        item = input("Enter item to add: ").strip()
        add_item(item)
    elif command == "remove":
        item = input("Enter item to remove: ").strip()
        remove_item(item)
    elif command == "display":
        display_inventory()
    elif command == "exit":
        break
    else:
        print("Invalid command. Please enter add/remove/display/exit.")

#3. Simple Inventory Management system
'''
- inventory is a global list
- function to add, remove and display items
- update inventory list as necessary 
'''
# Global variable to store the sum
total = 0

def calculate_sum(numbers):
    """Calculates the sum of a list of numbers and updates the global total."""
    global total
    total = sum(numbers)

def calculate_average(numbers):
    """Computes the average using the global total."""
    calculate_sum(numbers)  # Ensure total is updated
    if len(numbers) == 0:
        return 0  # Avoid division by zero
    return total / len(numbers)

# Main Program
numbers = []

while True:
    user_input = input("Enter a number (or type 'end' to finish): ").strip().lower()
    if user_input == "end":
        break
    if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
        numbers.append(int(user_input))
    else:
        print("Invalid input. Please enter a valid number.")

calculate_sum(numbers)
average = calculate_average(numbers)

print(f"Sum: {total}")
print(f"Average: {average}")
