import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url=os.getenv('LLM_BASE_URL'), api_key='lm-studio')
model = os.getenv('LLM_MODEL')

messages = [
    {
        'role':'system',
        'content':'Eres laura, una entrevistadora de recursos humanos amable. '
                    'Responde en español con una o dos frases cortas,'
                    'porque tus respuestas se van a leer en voz alta. ',
    },
    {'role': 'user','content':'Hola Laura, soy Javier y estoy listo para una entrevista. '},
]

start = time.perf_counter()
first_token = None
reply = ''

stream = client.chat.completions.create(
    model = model, messages=messages, stream=True, temperature=0.7
)
for chunk in stream:
    if not chunk.choices:
        continue
    text = chunk.choices[0].delta.content or ""
    if text and first_token is None:
        first_token = time.perf_counter() - start
    print(text, end='', flush=True)
    reply+=text
total = time.perf_counter() - start
print(f"\n\nPrimer token: {first_token:.2f}s | Total: {total:.2f} s")
