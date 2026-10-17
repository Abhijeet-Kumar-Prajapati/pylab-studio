import pyttsx3
import speech_recognition as sr
import webbrowser
import os  # Already imported
import socket

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    """Process the recognized command and perform actions."""
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open file" in command:
        file_path = "path_to_your_file.txt"  # Replace with the actual file path
        if os.path.exists(file_path):  # Check if file exists
            os.startfile(file_path)  # Open the file
            speak(f"Opening file: {file_path}")
        else:
            speak(f"The file {file_path} does not exist.")
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand the command.")

def listen():
    """Listen to the microphone and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                # Online recognition
                return recognizer.recognize_google(audio)
            except sr.RequestError:
                speak("I couldn't connect to the internet. Please check your connection.")
                return None
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand that.")
                return None
        except sr.WaitTimeoutError:
            speak("No speech detected within the timeout period.")
            return None

if __name__ == "__main__":
    speak("Initializing system. You can say commands like open Google, open file, or exit.")
    while True:
        try:
            command = listen()
            if command:
                process_command(command)
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")

def check_internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

if not check_internet():
    speak("No internet connection detected. Some features may not work.")
