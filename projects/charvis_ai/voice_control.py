import speech_recognition as sr
import os
import tkinter as tk
import tkinter.messagebox as messagebox

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the message box variable
message_box_visible = False
root = tk.Tk()
root.withdraw()  # Hide the main window

# Function to toggle message box visibility
def toggle_message_box():
    global message_box_visible
    if message_box_visible:
        root.withdraw()  # Hide the message box
        message_box_visible = False
    else:
        messagebox.showinfo('Info', 'This is a command message box.')
        message_box_visible = True

def listen_for_commands():
    with sr.Microphone() as source:
        print('Listening for commands...')
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f'You said: {command}')
            return command.lower()
        except sr.UnknownValueError:
            print('Could not understand the audio.')
            return None
        except sr.RequestError:
            print('Could not request results from Google Speech Recognition service.')
            return None

if __name__ == '__main__':
    while True:
        command = listen_for_commands()
        if command:
            if 'turn on' in command:
                print('Turning on...')  # Replace with actual functionality
                toggle_message_box()  # Show message box
            elif 'turn off' in command:
                print('Turning off...')  # Replace with actual functionality
                toggle_message_box()  # Hide message box
            elif 'exit' in command:
                break
