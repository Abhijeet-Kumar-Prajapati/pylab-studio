import pyttsx3
import speech_recognition as sr
import webbrowser
import Musiclibrary

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # Retrieve available voices

def set_voice(gender):
    """Set voice gender: 'male' or 'female'."""
    if gender.lower() == "male":
        engine.setProperty('voice', voices[0].id)  # Set male voice (typically first voice)
        speak("Voice set to male.")
        print("Voice set to: Male")
    elif gender.lower() == "female":
        engine.setProperty('voice', voices[1].id)  # Set female voice (typically second voice)
        speak("Voice set to female.")
        print("Voice set to: Female")
    else:
        speak("Invalid choice. Defaulting to male voice.")
        print("Invalid choice. Defaulting to Male voice.")
        engine.setProperty('voice', voices[0].id)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        if song in Musiclibrary.Music:
            link = Musiclibrary.Music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    # Prompt user to select a voice by speaking
    recognizer = sr.Recognizer()
    speak("Initializing computer. Please say male or female to select a voice.")
    print("Listening for voice selection...")

    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            voice_choice = recognizer.recognize_google(audio)
            set_voice(voice_choice)
    except Exception as e:
        print(f"Error during voice selection: {e}")
        speak("Error during voice selection. Defaulting to male voice.")
        set_voice("male")

    # Main loop to listen for commands
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "computer":
                    speak("Yes, how can I help?")
                    with sr.Microphone() as source:
                        print("Computer activated.")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        process_command(command)
        except Exception as e:
            print(f"Error: {e}")
            speak("I couldn't hear you clearly. Please try again.")
