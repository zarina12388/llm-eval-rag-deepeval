import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=0, timeout=30)

try:
    r = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[{"role": "user", "content": "Say the word READY and nothing else."}],
    )
    print(r.choices[0].message.content)
except Exception as e:
    print("ERROR TYPE:", type(e).__name__)
    print("ROOT CAUSE:", repr(e.__cause__))
    print("MESSAGE:", str(e)[:200])
