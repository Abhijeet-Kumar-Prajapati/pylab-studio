from reportlab.pdfgen import canvas

# File name for saving phone numbers in PDF format
pdf_file_name = "phone_contacts_restore.pdf"

# Function to save phone numbers in a PDF
def create_phone_numbers_pdf(file_name):
    """Creates a PDF file containing phone numbers ending with '50', incremented by 100."""
    # Create a canvas for the PDF
    c = canvas.Canvas(file_name)
    c.setFont("Helvetica", 10)  # Set font and size

    # Start coordinates for writing text
    x, y = 50, 800
    line_height = 12  # Spacing between lines

    # Generate numbers and add them to the PDF
    for i in range(10**9 + 50, 10**10, 100):
        c.drawString(x, y, str(i))  # Write the number at the current position
        y -= line_height  # Move to the next line

        # Check if the page is full, and if so, create a new page
        if y < 50:
            c.showPage()  # Save the current page
            y = 800  # Reset y-coordinate for the new page

    c.save()  # Save the PDF
    print(f"All numbers ending with '50' have been saved to '{file_name}'.")

# Main program execution
if __name__ == "__main__":
    create_phone_numbers_pdf(pdf_file_name)
