# File name for saving numbers
file_name = "contacts.bak"

# Open the file in write mode
with open(file_name, "w") as file:
    i = 1  # Starting number
    while i <= 9999999999:  # Loop until 9999999999
        file.write(f"{i:010}\n")  # Write the zero-padded number to the file
        i += 1  # Increment the counter

print(f"All numbers from 1 to 9999999999 have been saved to '{file_name}'.")
