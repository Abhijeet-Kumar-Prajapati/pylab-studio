import pyttsx3
import speech_recognition as sr
import webbrowser
import os  # Already imported
import socket
import speedtest  # Ensure the correct speedtest library is imported

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    """Process the recognized command and perform actions."""
    command = command.lower()
    
    # Voice commands for opening websites and files
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
    
    # Chatbot functionality: Respond to some basic questions
    elif "how are you" in command:
        speak("I am doing well, thank you for asking!")
    elif "what is your name" in command:
        speak("I am your assistant, here to help you with your tasks!")
    elif "hello" in command or "hi" in command:
        speak("Hello! How can I assist you today?")
    
    # Search functionality: Search on Google
    elif "search" in command:
        search_query = command.replace("search", "").strip()  # Extract the query after "search"
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching for {search_query} on Google.")
        else:
            speak("Please tell me what you would like to search for.")
    
    # Display internet speed
    elif "internet speed" in command:
        speed = check_internet_speed()
        speak(f"Your current internet speed is {speed} Mbps.")
    
    # Exit command
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    
    # If the command is not recognized
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

def check_internet_speed():
    """Check the internet speed using the speedtest-cli library."""
    st = speedtest.Speedtest()  # Correct way to initialize the Speedtest object
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert from bits/s to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bits/s to Mbps
    return round(download_speed, 2), round(upload_speed, 2)

def check_internet():
    """Check if the internet connection is available."""
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

if __name__ == "__main__":
    speak("Initializing system. You can say commands like open Google, open file, check internet speed, say hello, or exit.")
    while True:
        try:
            command = listen()
            if command:
                process_command(command)
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")

if not check_internet():
    speak("No internet connection detected. Some features may not work.")
