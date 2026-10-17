# # File name for saving phone numbers
# file_name = "phone_contacts_restore.txt"

# try:
#     # Open the file in write mode
#     with open(file_name, "w") as file:
#         # Start at the first ten-digit number ending in '60' and step by 100
#         for i in range(10**9 + 60, 10**10, 100):
#             file.write(f"{i}\n")  # Write the number to the file
#     print(f"All numbers ending with '60' have been saved to '{file_name}'")
# except Exception as e:
#     print(f"An error occurred: {e}")




# File name for saving contacts in Google CSV format
file_name = "phone_contacts_restore.csv"

# Open the file in write mode
with open(file_name, "w") as file:
    # Write the header for Google Contacts
    file.write("Name,Phone 1 - Value\n")
    
    # Generate contacts and write them in CSV format
    for i in range(10**9 + 50, 10**9 + 1060, 100):  # Example: First 10 contacts
        file.write(f"Contact {i},{i}\n")  # Write contact name and phone number

print(f"Google CSV contacts file saved to '{file_name}'")
