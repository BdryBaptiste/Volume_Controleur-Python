from comtypes import CLSCTX_INPROC_SERVER
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IMMDeviceEnumerator, AudioUtilities
from pycaw.constants import CLSID_MMDeviceEnumerator, DEVICE_STATE, EDataFlow, ERole, STGM
from pycaw.utils import AudioDevice
from ctypes import c_wchar_p

import policyconfig

class AudioDeviceManager:
    def __init__(self):
        self.devices = self.get_audio_devices()
        self.default_device = self.get_default_audio_device()

    def get_audio_devices(self):
        device_list = []
        deviceEnumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER
        )
        if deviceEnumerator is None:
            return devices

        devices = deviceEnumerator.EnumAudioEndpoints(
            EDataFlow.eRender.value, DEVICE_STATE.ACTIVE.value
        )
        if devices is None:
            return devices

        count = devices.GetCount()
        for i in range(count):
            device = devices.Item(i)
            dev = AudioUtilities.CreateDevice(device)
            device_list.append({
                'id': dev.id,
                'name': dev.FriendlyName
            })
        return device_list

    def get_default_audio_device(self):
        IMMDevice = AudioUtilities.GetSpeakers()
        device = AudioUtilities.CreateDevice(IMMDevice)
        return {
            'id': device.id,
            'name': device.FriendlyName
        }

    def set_default_audio_device(self, device_id, role=1):
        try:
            policy_config = comtypes.CoCreateInstance(
                policyconfig.CLSID_PolicyConfigClient,
                policyconfig.IPolicyConfig,
                CLSCTX_ALL
            )
            if policy_config is None:
                raise RuntimeError("Impossible d'initialiser PolicyConfigClient.")

            # Convertir device_id en LPCWSTR
            device_id_wstr = c_wchar_p(device_id)

            # Appel de la méthode COM
            result = policy_config.SetDefaultEndpoint(device_id_wstr, role)

            if result != 0:
                raise RuntimeError(f"Erreur lors du changement de périphérique: {result}")

            print(f"Périphérique audio changé : {device_id}")
            return True

        except Exception as e:
            print(f"Erreur : {e}")
            return False
