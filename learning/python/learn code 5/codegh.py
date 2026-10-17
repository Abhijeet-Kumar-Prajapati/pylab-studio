# File name for saving numbers
file_name = "number_list.txt"

# Function to create a list of numbers
def create_number_list(file_name):
    """
    Creates a file containing numbers from 0000000001 to 10000000000.
    """
    with open(file_name, "w") as file:
        # Generate numbers from 1 to 10^10
        for i in range(1, 10**10 + 1):
            file.write(f"{i:010}\n")  # Write each number as a zero-padded 10-digit string

    print(f"All numbers from 0000000001 to 10000000000 have been saved to '{file_name}'.")

# Main program execution
if __name__ == "__main__":
    create_number_list(file_name)
