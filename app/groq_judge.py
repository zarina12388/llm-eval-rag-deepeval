import os
from dotenv import load_dotenv
from groq import Groq
from deepeval.models import DeepEvalBaseLLM

load_dotenv()


class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def load_model(self):
        return self.client

    def generate(self, prompt, schema=None):
        if schema is None:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            return response.choices[0].message.content

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "Reply with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        text = response.choices[0].message.content.strip()
        return schema.model_validate_json(text)

    async def a_generate(self, prompt, schema=None):
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_name