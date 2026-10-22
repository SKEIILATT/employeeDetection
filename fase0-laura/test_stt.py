import glob
import os
import sys
import time

# Windows: make the CUDA DLLs installed by pip visible to CTranslate2
for d in glob.glob(os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "*", "bin")):
    os.add_dll_directory(d)
    os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]

import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
SECONDS = 5

print("Cargando modelo...")
model = WhisperModel("small", device="cuda", compute_type="int8")

print(f"Habla durante {SECONDS} segundos...")
audio = sd.rec(SECONDS * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1, dtype="float32")
sd.wait()
print("Transcribiendo...")

start = time.perf_counter()
segments, _ = model.transcribe(audio.flatten(), language="es", beam_size=1)
text = " ".join(s.text.strip() for s in segments)
elapsed = time.perf_counter() - start

print(f"\nTexto: {text}")
print(f"Tiempo de transcripción: {elapsed:.2f} s")
