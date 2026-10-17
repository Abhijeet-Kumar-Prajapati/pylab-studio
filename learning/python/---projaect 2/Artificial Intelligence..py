import pyttsx3                                          
import speech_recognition as sr                       
import webbrowser                                     
import Musiclibrary
recognizer = sr.Recognizer()                           
engine = pyttsx3.init() 
voices = engine.getProperty('voices')                               
def speak(text):                                           
    """Convert text to speech."""
    engine.say(text)                                        
    engine.runAndWait()
def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://fecebook.com")
    elif "youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
         song=c.lower().split(" ")[1]
         link =Musiclibrary.Music[song]
         webbrowser.open(link)
if __name__ == "__main__":                                       
   speak("intializing computer")
   while True:
        r =sr.Recognizer()
        print("recognizing....")
        try:
            with sr.Microphone() as source:
                   print("listening...") 
                    
                   audio = r. listen(source, timeout=2, phrase_time_limit=1) 
            word= r.recognize_google(audio)
            if(word.lower() == "computer"):
                 speak("Ya")

                 with sr.Microphone() as source:
                   print("computer activeted")
                   audio = r.listen(source)
                   command=r.recognize_google(audio)
                   processcommand(command)
        except Exception as e:
            print("Error;{0}".format(e))