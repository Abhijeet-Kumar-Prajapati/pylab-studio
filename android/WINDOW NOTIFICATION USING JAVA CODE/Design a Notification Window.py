import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling images

class NotificationWindow:
    def __init__(self, title, message, image_path=None):
        self.root = tk.Tk()
        self.root.title(title)
        
        # Set window size
        self.root.geometry("300x150")
        
        # Create a label for the message
        self.message_label = tk.Label(self.root, text=message, wraplength=250, font=("Helvetica", 12), fg="blue")
        self.message_label.pack(pady=10)
        
        # Optional image/icon
        if image_path:
            try:
                self.image = Image.open(image_path)
                self.image = self.image.resize((50, 50), Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(self.image)
                self.image_label = tk.Label(self.root, image=self.photo)
                self.image_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Create an OK button
        self.ok_button = tk.Button(self.root, text="OK", command=self.close)
        self.ok_button.pack(pady=10)

    def close(self):
        self.root.destroy()

def show_notification(title, message, image_path=None):
    try:
        notification = NotificationWindow(title, message, image_path)
        notification.root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    show_notification("Notification Title", "This is a sample notification message.", "path/to/image.png")