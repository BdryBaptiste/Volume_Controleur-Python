#to do later: issue -> need to figure out how to swtich audio device hint: https://github.com/KillerBOSS2019/TouchPortal-Windows-MediaMixer/blob/main/src/audioUtil/policyconfig.py


from pycaw.pycaw import AudioUtilities, MMDeviceEnumerator, EDataFlow, ERole

class AudioDeviceManager:
    def __init__(self):
        self.enumerator = MMDeviceEnumerator()
        self.devices = self.get_audio_devices()
        self.default_device = self.get_default_audio_device()

    def get_audio_devices(self):
        devices = self.enumerator.EnumAudioEndpoints(EDataFlow.eRender, 0)
        device_list = []
        for device in devices:
            device_list.append({
                'id': device.GetId(),
                'name': device.FriendlyName
            })
        return device_list

    def get_default_audio_device(self):
        device = self.enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia)
        return {
            'id': device.GetId(),
            'name': device.FriendlyName
        }

    def set_default_audio_device(self, device_id):
        print("Setting default audio device is not supported via Pycaw.")
