"""
Project manager module for handling project-related operations.
"""
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class ProjectManager:
    def __init__(self):
        # Define common project paths
        self.project_paths = {
            "documents": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "music": os.path.expanduser("~/Music"),
            "pictures": os.path.expanduser("~/Pictures"),
            "videos": os.path.expanduser("~/Videos")
        }

        # Define common applications with their paths
        self.applications = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        }

    def open_project_folder(self, folder_name):
        """Open a project folder in File Explorer."""
        try:
            folder_name = folder_name.lower()
            if folder_name in self.project_paths:
                path = self.project_paths[folder_name]
                if os.path.exists(path):
                    os.startfile(path)
                    logger.info(f"Opened folder: {path}")
                    return True, f"Opening {folder_name} folder"
                else:
                    return False, f"Folder {folder_name} not found"
            else:
                return False, "Unknown folder location"
        except Exception as e:
            logger.error(f"Error opening folder: {e}")
            return False, "Error opening folder"

    def open_application(self, app_name):
        """Open a specified application."""
        try:
            app_name = app_name.lower()
            if app_name in self.applications:
                app_path = os.path.expandvars(self.applications[app_name])
                if os.path.exists(app_path):
                    subprocess.Popen(app_path)
                    logger.info(f"Opened application: {app_name}")
                    return True, f"Opening {app_name}"
                else:
                    return False, f"Application {app_name} not found"
            else:
                return False, "Unknown application"
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return False, f"Error opening {app_name}"

    def add_custom_project(self, name, path):
        """Add a custom project path."""
        try:
            if os.path.exists(path):
                self.project_paths[name.lower()] = path
                return True, f"Added project: {name}"
            return False, "Invalid path"
        except Exception as e:
            logger.error(f"Error adding project: {e}")
            return False, "Error adding project"

    def add_custom_application(self, name, path):
        """Add a custom application path."""
        try:
            if os.path.exists(path):
                self.applications[name.lower()] = path
                return True, f"Added application: {name}"
            return False, "Invalid path"
        except Exception as e:
            logger.error(f"Error adding application: {e}")
            return False, "Error adding application"
