import random
import pandas as pd

def generate_numbers(count=1000):
    """Generates a list of 10-digit numbers ending in 84."""
    numbers = [str(random.randint(60000000, 99999999)) + "84" for _ in range(count)]
    return numbers

def save_to_excel(numbers, filename="phone_numbers.xlsx"):
    """Saves the list of numbers to an Excel file."""
    df = pd.DataFrame(numbers, columns=["Phone Numbers"])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    # Generate 1000 numbers ending in 84
    numbers = generate_numbers(1000)
    
    # Convert numbers to a format suitable for DataFrame
    data = [[num] for num in numbers]
    
    # Save to Excel
    save_to_excel(data)

if __name__ == "__main__":
    main()
