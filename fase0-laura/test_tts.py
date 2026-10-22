import time

import numpy as np
import sounddevice as sd
from piper import PiperVoice

VOICE = "models/es_MX-claude-high.onnx"
TEXT = (
    "Hola, soy Laura. Gracias por venir hoy. "
    "Para empezar, ¿podrías contarme un poco sobre ti y tu experiencia?"
)

voice = PiperVoice.load(VOICE)

start = time.perf_counter()
first_chunk = None
chunks = []
sample_rate = None
for chunk in voice.synthesize(TEXT):
    if first_chunk is None:
        first_chunk = time.perf_counter() - start
        sample_rate = chunk.sample_rate
    chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
total = time.perf_counter() - start

audio = np.concatenate(chunks)
duration = len(audio) / sample_rate
print(f"Primer fragmento: {first_chunk:.2f} s | Total: {total:.2f} s | Duración del audio: {duration:.1f} s")

sd.play(audio, sample_rate)
sd.wait()
