




# File name for saving numbers
file_name = "contacts_ending_with_60.bak"

# Function to generate numbers ending with '60'
def generate_numbers_ending_with_60(file_name):
    """Generates numbers from 1 to 9999999999 ending with '60' and saves them to a file."""
    batch_size = 10_000_000  # Number of numbers to write in each batch
    with open(file_name, "w") as file:
        buffer = []  # Temporary buffer to hold numbers
        # Generate numbers ending with '60'
        for i in range(1, 10_000_000_000, 100):  # Step by 100 to ensure the last two digits are '60'
            if str(i).endswith("60"):  # Check if the number ends with '60'
                buffer.append(f"{i:010}\n")  # Add zero-padded number to buffer
            if len(buffer) == batch_size:
                file.writelines(buffer)  # Write the buffer to the file in one operation
                buffer = []  # Clear the buffer
        if buffer:  # Write any remaining numbers in the buffer
            file.writelines(buffer)
    print(f"All numbers ending with '60' have been saved to '{file_name}'.")

# Main program execution
if __name__ == "__main__":
    generate_numbers_ending_with_60(file_name)
