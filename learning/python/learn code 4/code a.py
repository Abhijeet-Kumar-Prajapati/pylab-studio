



# File name for saving numbers
file_name = "contacts.bak"

# Function to generate and save numbers
def generate_numbers_fast(file_name):
    """
    Generates numbers from 1 to 9999999999 and saves them in a file efficiently.
    """
    batch_size = 10_000_000  # Number of numbers to write in each batch
    with open(file_name, "w") as file:
        buffer = []  # Temporary buffer to hold numbers
        for i in range(1, 10_000_000_000 + 1):  # Range from 1 to 9999999999
            buffer.append(f"{i:010}\n")  # Add zero-padded number to buffer
            if len(buffer) == batch_size:
                file.writelines(buffer)  # Write the buffer to the file in one operation
                buffer = []  # Clear the buffer
        if buffer:  # Write any remaining numbers in the buffer
            file.writelines(buffer)
    print(f"All numbers from 1 to 9999999999 have been saved to '{file_name}'.")

# Main program execution
if __name__ == "__main__":
    generate_numbers_fast(file_name)
