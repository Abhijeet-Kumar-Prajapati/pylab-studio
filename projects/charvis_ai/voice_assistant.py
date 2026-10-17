import pyttsx3
import speech_recognition as sr
import webbrowser
import logging
import time
from project_manager import ProjectManager
from music_library import get_song_url

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with text-to-speech and speech recognition."""
        try:
            # Initialize text-to-speech engine
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
            
            # Initialize speech recognition with optimized settings
            self.recognizer = sr.Recognizer()
            self.setup_recognition_settings()
            
            # Initialize project manager
            self.project_manager = ProjectManager()
            
            # Initialize microphone
            self.mic = None
            self.setup_microphone()
            
            # Set default voice
            self.set_voice("male")
            
        except Exception as e:
            logger.error(f"Error initializing voice assistant: {e}")
            raise

    def setup_recognition_settings(self):
        """Configure speech recognition settings for faster response."""
        # Lower energy threshold for easier activation
        self.recognizer.energy_threshold = 2500
        
        # Dynamic energy threshold for better adaptation
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        
        # Shorter pause threshold for faster command recognition
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.3

    def setup_microphone(self):
        """Setup and test microphone with optimized settings."""
        try:
            # List available microphones
            mics = sr.Microphone.list_microphone_names()
            logger.info(f"Available microphones: {mics}")
            
            if not mics:
                raise Exception("No microphones found")
            
            # Try to use the default microphone first
            try:
                self.mic = sr.Microphone(sample_rate=16000)  # Lower sample rate for faster processing
                self.test_microphone()
            except Exception as e:
                logger.warning(f"Default microphone failed: {e}")
                
                # Try each available microphone
                for index, name in enumerate(mics):
                    try:
                        logger.info(f"Trying microphone: {name}")
                        self.mic = sr.Microphone(device_index=index, sample_rate=16000)
                        self.test_microphone()
                        logger.info(f"Successfully using microphone: {name}")
                        break
                    except Exception as mic_error:
                        logger.warning(f"Failed to use microphone {name}: {mic_error}")
                        continue
                
            if self.mic is None:
                raise Exception("No working microphone found")
                
        except Exception as e:
            logger.error(f"Error setting up microphone: {e}")
            raise

    def listen(self, timeout=5, phrase_time_limit=5):
        """Listen for audio input with faster response times."""
        text = None
        try:
            with self.mic as source:
                logger.info("Listening...")
                # Quick ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, 
                                                 phrase_time_limit=phrase_time_limit)
                    logger.info("Processing speech...")
                    
                    # Try different recognition options for better accuracy
                    try:
                        # Try Google first (most accurate)
                        text = self.recognizer.recognize_google(audio)
                    except:
                        try:
                            # Fallback to Sphinx (offline, faster but less accurate)
                            text = self.recognizer.recognize_sphinx(audio)
                        except:
                            logger.warning("Speech recognition failed")
                            return None
                    
                    if text:
                        logger.info(f"Recognized: {text}")
                        return text.lower()
                        
                except sr.WaitTimeoutError:
                    logger.warning("Listening timed out")
                except sr.UnknownValueError:
                    logger.warning("Could not understand audio")
                except Exception as e:
                    logger.error(f"Error in speech recognition: {e}")
                
        except Exception as e:
            logger.error(f"Error in listen function: {e}")
        
        return None

    def speak(self, text, speed=180):
        """Convert text to speech with adjustable speed."""
        try:
            logger.info(f"Speaking: {text}")
            self.engine.setProperty('rate', speed)  # Adjust speaking speed
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")

    def test_microphone(self):
        """Quick microphone test."""
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            try:
                self.recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                logger.info("Microphone test successful")
            except sr.WaitTimeoutError:
                # This is actually okay - it means the mic is working but just didn't hear anything
                logger.info("Microphone test successful (no sound detected)")

    def set_voice(self, gender):
        """Set voice gender: 'male' or 'female'."""
        try:
            if gender.lower() == "male":
                self.engine.setProperty('voice', self.voices[0].id)
                self.speak("Voice set to male.")
                logger.info("Voice set to: Male")
            elif gender.lower() == "female":
                self.engine.setProperty('voice', self.voices[1].id)
                self.speak("Voice set to female.")
                logger.info("Voice set to: Female")
            else:
                self.speak("Invalid choice. Defaulting to male voice.")
                logger.warning("Invalid voice choice. Defaulting to Male voice.")
                self.engine.setProperty('voice', self.voices[0].id)
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            self.speak("Error setting voice. Using default.")

    def process_command(self, command):
        """Process and execute voice commands."""
        try:
            if not command:
                self.speak("I couldn't understand that. Please try again.")
                return

            command = command.lower()
            logger.info(f"Processing command: {command}")

            # Web commands
            if "open google" in command:
                webbrowser.open("https://google.com")
                self.speak("Opening Google")
            
            elif "open facebook" in command:
                webbrowser.open("https://facebook.com")
                self.speak("Opening Facebook")
            
            elif "open youtube" in command:
                webbrowser.open("https://youtube.com")
                self.speak("Opening YouTube")
            
            # Music commands
            elif command.startswith("play"):
                song = " ".join(command.split()[1:])  # Get everything after "play"
                url = get_song_url(song)
                if url:
                    webbrowser.open(url)
                    self.speak(f"Playing {song}")
                else:
                    self.speak("Sorry, I couldn't find that song.")
            
            # Project and application commands
            elif command.startswith("open"):
                # Extract the target name after "open"
                target = " ".join(command.split()[1:])
                
                # Try opening as application first
                success, message = self.project_manager.open_application(target)
                if success:
                    self.speak(message)
                else:
                    # If not an application, try opening as folder
                    success, message = self.project_manager.open_project_folder(target)
                    if success:
                        self.speak(message)
                    else:
                        self.speak(f"Sorry, I couldn't find {target}")
            
            # System commands
            elif "stop" in command or "exit" in command:
                self.speak("Goodbye!")
                return False
            
            else:
                self.speak("Sorry, I didn't understand that command.")
            
            return True

        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.speak("Sorry, there was an error processing your command.")
            return True

    def run(self):
        """Main loop for the voice assistant."""
        self.speak("Hello! I'm your voice assistant. Please wait while I adjust to your environment...")
        time.sleep(1)  # Give time for the message to be spoken
        
        self.speak("I'm ready now! Say 'computer' to activate me.")
        print("\nAvailable commands:")
        print("1. Say 'computer' to activate")
        print("2. After activation, you can use commands like:")
        print("   - 'open [application]' (e.g., 'open notepad', 'open chrome')")
        print("   - 'open [folder]' (e.g., 'open documents', 'open downloads')")
        print("   - 'play [song]' (e.g., 'play shape of you')")
        print("   - 'open [website]' (e.g., 'open google', 'open youtube')")
        print("   - 'stop' or 'exit' to quit\n")
        
        while True:
            try:
                command = self.listen(timeout=10, phrase_time_limit=5)
                if command and "computer" in command:
                    self.speak("Yes, how can I help?")
                    command = self.listen(timeout=5, phrase_time_limit=5)
                    if command:
                        if not self.process_command(command):
                            break
                    else:
                        self.speak("I'm still listening. Say 'computer' when you need me.")
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.speak("An error occurred. Please try again.")

if __name__ == "__main__":
    try:
        print("Starting Voice Assistant...")
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Critical error: {e}")
        print(f"Critical error occurred: {e}")
