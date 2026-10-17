import datetime
import json
import requests
import logging
import webbrowser
import subprocess
import os
import sys
import threading
import time
import urllib.parse
from urllib.parse import quote, urlencode
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from translate import Translator
import random
import speech_recognition as sr
import pyttsx3
import wikipedia
import wolframalpha
import pyjokes
from pytube import YouTube
import re
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from win10toast import ToastNotifier

class CharvisAI:
    def __init__(self):
        """Initialize Charvis AI with enhanced capabilities."""
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)  # Default male voice
        self.engine.setProperty('rate', 180)  # Speed of speech
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Increased sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.microphone = sr.Microphone()
        
        # Voice and language settings
        self.voice_gender = "male"
        self.current_language = "english"
        self.translator = Translator(to_lang="en")
        
        # Media settings
        self.media_quality = "high"  # Default quality
        self.volume_level = 0.7  # Default volume (70%)
        
        # Chat context and templates
        self.chat_context = []
        self.max_context_length = 5
        self.conversation_templates = {
            "greetings": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?"
            ],
            "acknowledgments": [
                "I understand. Let me help you with that.",
                "Got it. I'll take care of that for you.",
                "Sure, I can help you with that."
            ],
            "confirmations": [
                "Task completed successfully!",
                "Done! Is there anything else you need?",
                "All set! What would you like to do next?"
            ]
        }
        
        # Command keywords
        self.keywords = {
            "youtube": ["youtube", "play video", "watch"],
            "google": ["google", "search google", "look up"],
            "music": ["play music", "play song", "play audio"],
            "volume": ["volume up", "volume down", "set volume"],
            "quality": ["high quality", "medium quality", "low quality"],
            "download": ["download music", "download video", "download song"],
            "voice": ["male voice", "female voice", "change voice"],
            "language": ["speak in", "change language", "switch to"],
            "system": ["shutdown", "restart", "sleep", "lock computer"]
        }
        
        # Media directories
        self.media_paths = {
            "music": os.path.join(os.path.expanduser("~"), "Music"),
            "videos": os.path.join(os.path.expanduser("~"), "Videos"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads")
        }
        
        # Initialize logging
        logging.basicConfig(
            filename='charvis.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize notification system
        self.toaster = ToastNotifier()
        self.message_queue = []
        self.current_message = None
        
        # Start background listener
        self.is_listening = False
        self.background_thread = None
        
        # GUI elements
        self.window = None
        self.command_entry = None
        self.command_log = None
        self.setup_gui()
        self.create_control_panel()
        
    def setup_gui(self):
        """Setup GUI window with Iron Man-style interface."""
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.window = ctk.CTk()
        self.window.title("C.H.A.R.V.I.S")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a1a")
        
        # Bring window to front
        self.window.lift()
        self.window.focus_force()
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create message display area at top
        self.message_frame = ctk.CTkFrame(main_frame, fg_color="#002233", height=60)
        self.message_frame.pack(fill=tk.X, pady=(0, 20))
        self.message_frame.pack_propagate(False)
        
        self.message_label = ctk.CTkLabel(
            self.message_frame,
            text="",
            font=("Rajdhani", 16, "bold"),
            text_color="#00ff00"
        )
        self.message_label.pack(fill=tk.BOTH, expand=True)
        
        # Create title with glowing effect
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="C.H.A.R.V.I.S",
            font=("Rajdhani", 36, "bold"),
            text_color="#00a8e8"
        )
        title_label.pack()
        
        # Create command log frame with sci-fi styling
        log_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Command log with custom styling
        self.command_log = tk.Text(
            log_frame,
            height=15,
            bg="#2d2d2d",
            fg="#00a8e8",
            font=("Consolas", 10),
            wrap=tk.WORD,
            borderwidth=0,
            insertbackground="#00a8e8"
        )
        self.command_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create input frame with prominent styling
        input_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", height=60)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        input_frame.pack_propagate(False)  # Maintain height
        
        # Modern command entry with improved visibility
        self.command_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your command here...",
            font=("Rajdhani", 16),
            height=40,
            border_color="#00a8e8",
            fg_color="#1a1a1a",
            text_color="#ffffff",
            placeholder_text_color="#4a4a4a"
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.command_entry.bind('<Return>', self.handle_text_command)
        
        # Modern execute button
        send_button = ctk.CTkButton(
            input_frame,
            text="EXECUTE",
            font=("Rajdhani", 14, "bold"),
            height=40,
            fg_color="#00a8e8",
            hover_color="#0077cc",
            command=self.handle_text_command
        )
        send_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Status bar with improved visibility
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready for your command",
            font=("Rajdhani", 14),
            text_color="#00a8e8"
        )
        self.status_label.pack(fill=tk.X)
        
        # Focus on the text entry
        self.command_entry.focus_set()
        
    def create_control_panel(self):
        """Create floating control button with expandable panel."""
        # Create floating button window
        self.control_button = ctk.CTkToplevel()
        self.control_button.title("")
        self.control_button.geometry("60x60")
        self.control_button.resizable(False, False)
        self.control_button.attributes('-topmost', True)
        self.control_button.overrideredirect(True)  # Remove window decorations
        
        # Style the button window
        self.control_button.configure(fg_color="#1a1a1a")
        
        # Create circular button
        button_frame = ctk.CTkFrame(self.control_button, fg_color="#00a8e8", corner_radius=30)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Charvis icon/label
        icon_label = ctk.CTkLabel(
            button_frame,
            text="C",
            font=("Rajdhani", 24, "bold"),
            text_color="#ffffff"
        )
        icon_label.pack(expand=True)
        
        # Create expandable control panel
        self.control_panel = ctk.CTkToplevel()
        self.control_panel.title("")
        self.control_panel.geometry("200x280")
        self.control_panel.resizable(False, False)
        self.control_panel.attributes('-topmost', True)
        self.control_panel.overrideredirect(True)  # Remove window decorations
        self.control_panel.withdraw()  # Hide initially
        
        # Style the control panel
        self.control_panel.configure(fg_color="#1a1a1a")
        
        # Add a border effect
        border_frame = ctk.CTkFrame(self.control_panel, fg_color="#00a8e8")
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create controls frame
        controls_frame = ctk.CTkFrame(border_frame, fg_color="#1a1a1a")
        controls_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Title with close button
        title_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        title = ctk.CTkLabel(
            title_frame,
            text="C.H.A.R.V.I.S",
            font=("Rajdhani", 20, "bold"),
            text_color="#00a8e8"
        )
        title.pack(side=tk.LEFT)
        
        close_btn = ctk.CTkButton(
            title_frame,
            text="×",
            width=30,
            height=30,
            font=("Arial", 16, "bold"),
            fg_color="#1a1a1a",
            hover_color="#ff3333",
            command=lambda: self.control_panel.withdraw()
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Main controls
        main_controls = ctk.CTkFrame(controls_frame, fg_color="transparent")
        main_controls.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toggle main window button
        self.toggle_button = ctk.CTkButton(
            main_controls,
            text="Hide Charvis",
            font=("Rajdhani", 14),
            height=40,
            fg_color="#00a8e8",
            hover_color="#0077cc",
            command=self.toggle_main_window
        )
        self.toggle_button.pack(pady=(0, 10), fill=tk.X)
        
        # Voice control button
        self.voice_toggle = ctk.CTkButton(
            main_controls,
            text="Start Listening",
            font=("Rajdhani", 14),
            height=40,
            fg_color="#00a8e8",
            hover_color="#0077cc",
            command=self.toggle_voice_listening
        )
        self.voice_toggle.pack(pady=(0, 10), fill=tk.X)
        
        # Quick command buttons
        quick_commands = [
            ("🎵 YouTube", "youtube"),
            ("🔍 Google", "google"),
            ("⏰ Time", "what time is it"),
            ("❓ Help", "show help")
        ]
        
        for label, command in quick_commands:
            btn = ctk.CTkButton(
                main_controls,
                text=label,
                font=("Rajdhani", 14),
                height=30,
                fg_color="#2d2d2d",
                hover_color="#3d3d3d",
                border_color="#00a8e8",
                border_width=1,
                command=lambda cmd=command: self.process_command(cmd)
            )
            btn.pack(pady=5, fill=tk.X)
        
        # Make the button draggable
        for widget in (button_frame, icon_label):
            widget.bind('<Button-1>', self.start_drag)
            widget.bind('<B1-Motion>', self.on_drag)
        
        # Toggle panel on button click
        for widget in (button_frame, icon_label):
            widget.bind('<Button-1>', self.toggle_control_panel)
        
        # Position initial control button in top-right corner
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.control_button.geometry(f"+{screen_width-70}+{screen_height//4}")
        
    def start_drag(self, event):
        """Start dragging the control button."""
        self.drag_data = {'x': event.x, 'y': event.y}
        
    def on_drag(self, event):
        """Handle dragging of the control button."""
        if hasattr(self, 'drag_data'):
            x = self.control_button.winfo_x() + (event.x - self.drag_data['x'])
            y = self.control_button.winfo_y() + (event.y - self.drag_data['y'])
            self.control_button.geometry(f"+{x}+{y}")
        
    def toggle_control_panel(self, event=None):
        """Toggle the control panel visibility."""
        if self.control_panel.winfo_viewable():
            self.control_panel.withdraw()
        else:
            # Position panel next to the button
            x = self.control_button.winfo_x() - 210  # Panel width + margin
            y = self.control_button.winfo_y()
            self.control_panel.geometry(f"+{x}+{y}")
            self.control_panel.deiconify()
            self.control_panel.lift()
            
    def toggle_main_window(self):
        """Toggle main window visibility."""
        if self.minimized:
            self.window.deiconify()
            self.window.lift()
            self.toggle_button.configure(text="Hide Charvis")
            self.minimized = False
            self.show_message("Charvis interface restored")
        else:
            self.window.iconify()
            self.toggle_button.configure(text="Show Charvis")
            self.minimized = True
            self.show_message("Charvis interface minimized")
            
    def animate_startup(self):
        """Create Iron Man-style startup animation."""
        def type_text(text, widget, speed=50):
            if not text:
                return
            widget.insert(tk.END, text[0])
            widget.see(tk.END)
            self.window.after(speed, type_text, text[1:], widget)
        
        startup_text = """
=== C.H.A.R.V.I.S INITIALIZATION SEQUENCE ===
> Loading core systems...
> Initializing voice recognition...
> Calibrating response algorithms...
> Establishing neural networks...
> All systems operational.

Ready to assist, sir.
        """
        self.command_log.delete(1.0, tk.END)
        type_text(startup_text.strip(), self.command_log)
        
    def log_command(self, command, response=None):
        """Log command and response with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.command_log.insert(tk.END, f"\n[{timestamp}] Command: {command}\n")
        if response:
            self.command_log.insert(tk.END, f"Response: {response}\n")
        self.command_log.see(tk.END)
        
    def toggle_voice_listening(self):
        """Toggle voice listening on/off."""
        if not self.is_listening:
            self.start_background_listener()
            self.voice_indicator.configure(text="🎤 Voice: Active", text_color="#00ff00")
            self.voice_button.configure(text="Stop Listening")
            self.log_command("System", "Voice recognition activated")
        else:
            self.is_listening = False
            if self.background_thread:
                self.background_thread.join()
            self.voice_indicator.configure(text="🎤 Voice: Standby", text_color="#666666")
            self.voice_button.configure(text="Start Listening")
            self.log_command("System", "Voice recognition deactivated")

    def start_background_listener(self):
        """Start background listening for wake word."""
        self.is_listening = True
        self.background_thread = threading.Thread(target=self._background_listen)
        self.background_thread.daemon = True
        self.background_thread.start()
        
    def _background_listen(self):
        """Background listening function with visual feedback."""
        while self.is_listening:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source)
                    
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    self.window.after(0, self.handle_voice_command, command)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.window.after(0, self.log_command, "System", "Could not request results from speech recognition service")
            except Exception as e:
                self.window.after(0, self.log_command, "System", f"Error in voice recognition: {str(e)}")
                time.sleep(1)

    def handle_voice_command(self, command):
        """Handle voice commands with visual feedback."""
        self.log_command("Voice", command)
        self.status_label.configure(text=f"Processing voice command: {command}")
        self.process_command(command)
        self.status_label.configure(text="System Ready")

    def process_command(self, command):
        """Process voice commands with enhanced features."""
        try:
            # Show command in message area
            self.show_message(f"Processing: {command}")
            
            # Check for shutdown command
            if any(word in command.lower() for word in ["turn off", "shutdown", "exit", "quit"]):
                self.shutdown()
                
            # YouTube commands
            if any(keyword in command.lower() for keyword in ["youtube", "play video", "watch"]):
                query = command.lower()
                for keyword in ["youtube", "play", "video", "watch"]:
                    query = query.replace(keyword, "").strip()
                if query:
                    self.log_command("System", f"Searching YouTube for: {query}")
                    self.play_youtube(query)
                else:
                    self.speak("Please specify what you'd like to watch on YouTube")
                return

            # Google Search commands
            if any(keyword in command.lower() for keyword in ["google", "search", "look up"]):
                query = command.lower()
                for keyword in ["google", "search", "look up"]:
                    query = query.replace(keyword, "").strip()
                if query:
                    self.log_command("System", f"Searching Google for: {query}")
                    self.google_search(query)
                else:
                    self.speak("Please specify what you'd like to search for")
                return

            # Music commands
            elif any(keyword in command for keyword in self.keywords["music"]):
                song = command.split("play")[-1].strip()
                self.play_media(song, media_type="music")
                
            # Quality settings
            elif any(keyword in command for keyword in self.keywords["quality"]):
                if "high" in command:
                    self.media_quality = "high"
                elif "medium" in command:
                    self.media_quality = "medium"
                else:
                    self.media_quality = "low"
                self.speak(f"Quality set to {self.media_quality}")
                
            # Download commands
            elif any(keyword in command for keyword in self.keywords["download"]):
                query = command.split("download")[-1].strip()
                media_type = "video" if "video" in command else "music"
                self.download_media(query, media_type)
                
            # Voice commands
            elif any(keyword in command for keyword in self.keywords["voice"]):
                if "male" in command:
                    self.change_voice("male")
                elif "female" in command:
                    self.change_voice("female")
                    
            # Language commands
            elif any(keyword in command for keyword in self.keywords["language"]):
                for lang in ["english", "hindi", "spanish", "french", "german"]:
                    if lang in command:
                        self.change_language(lang)
                        break
                        
            # System commands
            elif any(keyword in command for keyword in self.keywords["system"]):
                self.handle_system_command(command)
                
            # Question answering
            elif any(word in command for word in ["what", "who", "when", "where", "why", "how"]):
                answer = self.get_answer(command)
                self.speak(answer)
                
            # Chat response for other commands
            else:
                response = self.chat_response(command)
                self.speak(response)
                
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            self.speak("I encountered an error processing your command")
            
    def shutdown(self):
        """Properly shutdown Charvis AI."""
        self.is_listening = False
        if self.background_thread and self.background_thread.is_alive():
            self.background_thread.join()
        self.speak("Shutting down. Goodbye!")
        if self.window:
            self.window.destroy()
        if self.control_panel:
            self.control_panel.destroy()
        sys.exit(0)

    def play_youtube(self, query):
        """Enhanced YouTube search and play functionality."""
        try:
            # Create search URL
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            
            # Use custom HTML to create a better-looking message
            html_message = f"""
            <div style='font-family: Rajdhani, sans-serif; color: #00a8e8; padding: 10px;'>
                🎵 Opening YouTube Search
                <br>Query: {query}
            </div>
            """
            self.log_command("YouTube", html_message)
            
            # Open in default browser
            webbrowser.open(search_url)
            self.speak(f"Opening YouTube search for {query}")
        except Exception as e:
            self.log_command("Error", f"Failed to open YouTube: {str(e)}")
            self.speak("I encountered an error while trying to open YouTube")

    def google_search(self, query):
        """Enhanced Google search functionality."""
        try:
            # Create search URL
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            
            # Use custom HTML to create a better-looking message
            html_message = f"""
            <div style='font-family: Rajdhani, sans-serif; color: #00a8e8; padding: 10px;'>
                🔍 Opening Google Search
                <br>Query: {query}
            </div>
            """
            self.log_command("Google", html_message)
            
            # Open in default browser
            webbrowser.open(search_url)
            self.speak(f"Opening Google search for {query}")
        except Exception as e:
            self.log_command("Error", f"Failed to open Google search: {str(e)}")
            self.speak("I encountered an error while trying to search Google")

    def change_voice(self, gender):
        """Change voice gender."""
        try:
            voices = self.engine.getProperty('voices')
            if gender == "male":
                self.engine.setProperty('voice', voices[0].id)
                self.voice_gender = "male"
            else:
                self.engine.setProperty('voice', voices[1].id)
                self.voice_gender = "female"
            self.speak(f"Voice changed to {gender}")
        except Exception as e:
            self.logger.error(f"Error changing voice: {e}")
            
    def speak(self, text):
        """Enhanced speak function with visual feedback."""
        self.show_message(text, notification=True)
        self.log_command("System", text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def play_notification_sound(self):
        """Play a notification sound."""
        # Add your notification sound code here
        pass
        
    def play_listening_sound(self):
        """Play a sound to indicate listening."""
        # Add your listening sound code here
        pass
        
    def handle_system_command(self, command):
        """Handle system-related commands."""
        if "shutdown" in command:
            self.speak("Shutting down the computer")
            os.system("shutdown /s /t 60")
        elif "restart" in command:
            self.speak("Restarting the computer")
            os.system("shutdown /r /t 60")
        elif "sleep" in command:
            self.speak("Putting computer to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif "lock" in command:
            self.speak("Locking the computer")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            
    def handle_text_command(self, event=None):
        """Handle commands from text input with visual feedback."""
        command = self.command_entry.get()
        if command:
            self.command_entry.delete(0, tk.END)
            self.status_label.configure(text=f"Processing: {command}")
            self.log_command(command)
            self.process_command(command)
            self.status_label.configure(text="System Ready")
            
    def show_message(self, message, duration=3000, notification=True):
        """Show message at top of screen and optionally as desktop notification."""
        # Update message label with new text
        self.message_label.configure(text=message)
        
        # Show Windows notification if requested
        if notification:
            try:
                self.toaster.show_toast(
                    "C.H.A.R.V.I.S",
                    message,
                    duration=duration/1000,
                    threaded=True
                )
            except Exception as e:
                self.logger.error(f"Failed to show notification: {e}")
        
        # Clear message after duration
        self.window.after(duration, lambda: self.message_label.configure(text=""))
        
    def run(self):
        """Start Charvis AI with focus on text interface."""
        self.speak("Charvis interface ready. Control panel activated.")
        self.log_command("System", "💻 Text interface and control panel active")
        self.status_label.configure(text="Type your command and press Enter or click EXECUTE")
        
        # Position control panel in top-right corner
        screen_width = self.window.winfo_screenwidth()
        self.control_panel.geometry(f"+{screen_width-220}+10")
        
        try:
            self.window.mainloop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            self.shutdown()
            
if __name__ == "__main__":
    charvis = CharvisAI()
    charvis.run()
