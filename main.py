import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
   verbose = '--verbose' in sys.argv
   
   prompt_parts = [arg for arg in sys.argv[1:] if arg != '--verbose']
   prompt = ' '.join(prompt_parts)

   messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
   ]

   response = client.models.generate_content(
      model='gemini-2.0-flash-001', contents=messages
   )

   if len(sys.argv) < 2:
      print("Error: No prompt provided")
      sys.exit(1)

   if verbose:
      print(f'User prompt: "{prompt}"')
      print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
      print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

   print(response.text)

if __name__ == "__main__":
    main()