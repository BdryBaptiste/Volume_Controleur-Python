from AudioController import AudioController
from AppManager import AppManager

audio_controller = AudioController("chrome.exe")
audio_controller.get_process_volume
audio_controller.set_volume(1.0)
audio_controller.mute()
audio_controller.unmute()

app_manager = AppManager()
app_manager.update_applications()
print(app_manager.get_applications())