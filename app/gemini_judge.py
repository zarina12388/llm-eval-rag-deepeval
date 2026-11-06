import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from deepeval.models import DeepEvalBaseLLM

load_dotenv()


class GeminiJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def load_model(self):
        return self.client

    def generate(self, prompt, schema=None):
        if schema is None:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            return response.text

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.strip("`").removeprefix("json").strip()
        return schema.model_validate_json(text)

    async def a_generate(self, prompt, schema=None):
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_name