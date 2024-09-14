# See the list of input devices

import pyaudio

p = pyaudio.PyAudio()

#print("\n\n\n Input Devices:  ",p.get_device_count()")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")

p.terminate()