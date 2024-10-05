# app_manager.py

from pycaw.pycaw import AudioUtilities
from AudioController import AudioController

class AppManager:
    def __init__(self):
        self.applications = {}  # Dictionnaire des applications et de leurs contrôleurs

    def update_applications(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                process_name = session.Process.name()
                if process_name not in self.applications:
                    self.applications[process_name] = AudioController(process_name)

    def get_applications(self):
        return list(self.applications.keys())

    def get_controller(self, process_name):
        return self.applications.get(process_name)
