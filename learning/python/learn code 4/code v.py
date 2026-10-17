# # # # Generate a list of 10-digit numbers
# # # numbers = list(range(1000000000, 1000000100))  # Example: generating 100 numbers starting from 1,000,000,000

# # # # Print the last 50 numbers
# # # print("Last 50 numbers:")
# # # for num in numbers[-50:]:
# # #     print(num)


# # # Generate a list of 10-digit numbers
# # numbers = list(range(1000000000, 1000000100))  # Example: Generating 100 numbers starting from 1,000,000,000

# # # Print all 10-digit numbers
# # print("Generated 10-digit numbers:")
# # for num in numbers:
# #     print(num)

# # # Extract the last 50 numbers
# # last_50_numbers = numbers[-50:]  # Slicing to get the last 50 numbers

# # # Print the last 50 numbers
# # print("\nLast 50 numbers:")
# # for num in last_50_numbers:
# #     print(num)


# # Generate a list of 10-digit numbers
# numbers = list(range(1000000000, 1000000050))  # Fixed 50 numbers starting from 1,000,000,000

# # Print all the 10-digit numbers
# print("All 10-digit numbers:")
# for num in numbers:
#     print(num)

# # Verify the last 50 numbers (which are the entire list in this case)
# print("\nLast 50 numbers (unchanged):")
# for num in numbers[-50:]:
#     print(num)