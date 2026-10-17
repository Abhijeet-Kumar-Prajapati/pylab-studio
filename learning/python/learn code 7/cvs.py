# Generate a CSV file with contacts from 1000000050 to 9999999999
output_csv = "contacts_restore.csv"

with open(output_csv, "w") as file:
    file.write("Name,Phone\n")  # CSV header
    i = 1
    while i <= 9999999999:
        file.write(f"Contact {i},{i}\n")
        i += 100  # Increment by 100 for example, adjust as needed

print(f"CSV file '{output_csv}' created with contacts from {1} to {9999999999}.")
