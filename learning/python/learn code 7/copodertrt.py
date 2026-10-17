# # Sample contact data
# contacts = [
#     {"name": "John Doe", "phone": "123-456-7890", "email": "john@example.com"},
#     {"name": "Jane Smith", "phone": "987-654-3210", "email": "jane@example.com"},
# ]

# # Write contacts to a .bak file
# with open('contacts.bak', 'w') as file:
#     for contact in contacts:
#         file.write(f"Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}\n")

# print("Contacts have been exported to contacts.bak")



i = 1
with open("output.txt", "w") as file:  # Create or overwrite "output.txt"
    while i < 9999999999:  # Adjust range for practical testing (avoid huge numbers)
        file.write(f"{i}\n")  # Write the number followed by a newline
        i += 1  # Increment
print("File 'output.txt' created successfully!")
import csv

input_file = "contacts_restore.csv"  # Your CSV file
output_file = "contacts.vcf"         # Output VCF file

with open(input_file, "r") as csv_file, open(output_file, "w") as vcf_file:
    reader = csv.DictReader(csv_file)  # Read CSV file as a dictionary
    for row in reader:
        vcf_file.write("BEGIN:VCARD\n")
        vcf_file.write("VERSION:3.0\n")
        vcf_file.write(f"FN:{row['Name']}\n")  # Full name
        vcf_file.write(f"TEL;TYPE=PHONE:{row['Phone']}\n")  # Phone number
        if 'Email' in row and row['Email']:  # Include email if it exists
            vcf_file.write(f"EMAIL:{row['Email']}\n")
        vcf_file.write("END:VCARD\n")

print("VCF file created successfully!")
