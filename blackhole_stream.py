import pyaudio
import sys

CHUNK = 1024
CHANNELS = 1
RATE = 48000
DEVICE_NAME = "BlackHole"

p = pyaudio.PyAudio()

device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if DEVICE_NAME.lower() in info['name'].lower() and info['maxInputChannels'] > 0:
        device_index = i
        print(f"Znaleziono: {info['name']} (index {i})", file=sys.stderr)
        break

if device_index is None:
    print("BLAD: Nie znaleziono BlackHole!", file=sys.stderr)
    sys.exit(1)

stream = p.open(
    format=pyaudio.paFloat32,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=device_index,
    frames_per_buffer=CHUNK
)

print("Streaming audio...", file=sys.stderr)

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()