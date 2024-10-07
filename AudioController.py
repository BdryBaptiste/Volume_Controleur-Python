from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
from io import BytesIO


class AudioController:
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.get_process_volume()
        self.exe_path = self.get_exe_path()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

    def get_process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug

    def extract_icon(self):
        if not self.exe_path:
            print(f"Chemin exécutable non trouvé pour {self.process_name}")
            return None

        try:
            large, small = win32gui.ExtractIconEx(self.exe_path, 0)
            if large:
                hicon = large[0]
            elif small:
                hicon = small[0]
            else:
                return None

            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 256, 256)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            win32gui.DrawIconEx(hdc.GetSafeHdc(), 0, 0, hicon, 256, 256, 0, None, win32con.DI_NORMAL)
            win32gui.DestroyIcon(hicon)

            bmpinfo = hbmp.GetInfo()
            bmpstr = hbmp.GetBitmapBits(True)
            img = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA', 0, 1)

            # Sauvegarder l'image dans un buffer
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            return img_io
        except Exception as e:
            print(f"Erreur lors de l'extraction de l'icône : {e}")
            return None
        
    def get_exe_path(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == self.process_name:
                return session.Process.exe()
        return None
    
    def is_muted(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == self.process_name:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                is_muted = volume.GetMute()
                return bool(is_muted)
        return False
