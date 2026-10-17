import os
import sys
import subprocess
import time
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charvis_startup.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_charvis():
    """Start Charvis AI and handle any crashes."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        charvis_path = os.path.join(script_dir, 'charvis_ai.py')
        
        # Activate virtual environment if it exists
        venv_path = os.path.join(script_dir, 'venv')
        if os.path.exists(venv_path):
            if sys.platform == 'win32':
                python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
            else:
                python_path = os.path.join(venv_path, 'bin', 'python')
        else:
            python_path = sys.executable
        
        logging.info(f"Starting Charvis AI at {datetime.now()}")
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Function to show all features
        def show_features():
            features = "1. Feature One\n2. Feature Two\n3. Feature Three"
            messagebox.showinfo('Charvis Features', features)

        # Create a button to show features
        features_button = tk.Button(root, text='Show Features', command=show_features)
        features_button.pack(pady=10)
        
        # Show the message box
        messagebox.showinfo('Information', 'This is a message box!')
        messagebox.showinfo('Another Message', 'This is another message box!')
        
        # Show the message box about desktop icons
        messagebox.showinfo('Desktop Icons', 'Here are your desktop icons!')
        
        # Create a text box to show a message about desktop icons
        text_box = tk.Toplevel(root)
        text_box.title("Desktop Icons")
        text_box_label = tk.Label(text_box, text="Here are your desktop icons!")
        text_box_label.pack(padx=10, pady=10)
        
        while True:  # Keep trying to restart if Charvis crashes
            try:
                # Start Charvis
                process = subprocess.Popen(
                    [python_path, charvis_path],
                    cwd=script_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # Log process output
                while process.poll() is None:
                    output = process.stdout.readline()
                    if output:
                        logging.info(output.strip())
                    error = process.stderr.readline()
                    if error:
                        logging.error(error.strip())
                
                # If Charvis exits, wait before restarting
                if process.returncode != 0:
                    logging.warning(f"Charvis exited with code {process.returncode}. Restarting in 5 seconds...")
                    time.sleep(5)
                else:
                    logging.info("Charvis exited normally")
                    break
                    
            except Exception as e:
                logging.error(f"Error running Charvis: {e}")
                time.sleep(5)  # Wait before retrying
                
    except Exception as e:
        logging.error(f"Critical error in start_charvis: {e}")

if __name__ == "__main__":
    start_charvis()
