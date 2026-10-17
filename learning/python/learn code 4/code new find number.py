# # for i in range(10**9, 10**10):  # Only loop through ten-digit numbers
# #     if i % 100 == 50:  # Check if the last two digits are 60
# #         print(i)


# # # File name for saving phone numbers
# # file_name = "phone_contacts_restore.txt"

# # # Open the file in write mode
# # with open(file_name, "w") as file:
# #     # Iterate through the range of ten-digit numbers
# #     for i in range(10**9, 10**10):
# #         if i % 100 == 60:  # Check if the number ends with 60
# #             file.write(f"{i}\n")  # Write the number to the file

# # print(f"All numbers ending with '60' have been saved to {file_name}")




# # # File name for saving phone numbers
# # file_name = "phone_contacts_restore.txt"

# # # Open the file in write mode
# # with open(file_name, "w") as file:
# #     # Start at the first ten-digit number ending in '50' and step by 100
# #     for i in range(10**9 + 50, 10**10, 100):
# #         file.write(f"{i}\n")  # Write the number to the file

# # print(f"All numbers ending with '50' have been saved to {file_name}")




# # File name for saving phone numbers
# file_name = "phone_contacts_restore.txt"

# # Function to create the file with numbers
# def create_phone_numbers_file(file_name):
#     """Creates a file containing phone numbers ending with '50', starting from 1 to 10^10."""
#     with open(file_name, "w") as file:
#         # Generate numbers ending with '50', starting from 1 and up to 10^10
#         for i in range(1, 10**10 + 1):
#             if str(i).endswith("50"):  # Check if the number ends with '50'
#                 file.write(f"{i}\n")  # Write each number to the file

#     print(f"All numbers ending with '50' have been saved to '{file_name}'.")

# # Function to search for a specific number in the file
# def search_number(file_name, target_number):
#     """Searches for a specific number in the generated file."""
#     with open(file_name, "r") as file:
#         numbers = file.readlines()
#         # Check if the target number exists in the list
#         if f"{target_number}\n" in numbers:
#             position = numbers.index(f"{target_number}\n") + 1
#             print(f"The number {target_number} is found at position {position}.")
#         else:
#             print(f"The number {target_number} is not in the sequence.")

# # Main program execution
# if __name__ == "__main__":
#     # Step 1: Create the file with numbers
#     create_phone_numbers_file(file_name)

#     # Step 2: Allow the user to search for a number
#     target_number = input("\nEnter a number to search: ")
#     if target_number.isdigit():
#         search_number(file_name, target_number)
#     else:
#         print("Please enter a valid numeric value.")




