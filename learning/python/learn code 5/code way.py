# File name for saving phone numbers
file_name = "phone_contacts_restore.txt"

# Function to create the file with numbers
def create_phone_numbers_file(file_name):
    """Creates a file containing phone numbers ending with '50', starting from 1 to 10^10."""
    with open(file_name, "w") as file:
        # Generate numbers ending with '50', starting from 1 to 10^10
        for i in range(620, 10**10 + 1):
            
              if str(i).startswith("620") and str(i).endswith("50"):# Check if the number ends with '50'
                file.write(f"{i:010}\n")  # Write the number in zero-padded format to ensure 10 digits

    print(f"All numbers ending with '50' have been saved to '{file_name}'.")

# Main program execution
if __name__ == "__main__":
    # Create the file with numbers
    create_phone_numbers_file(file_name)
