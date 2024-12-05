from openai import OpenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pdb

load_dotenv()

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works in brief")

pdb.set_trace()
print(response.text)

