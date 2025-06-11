import os
from dotenv import load_dotenv
from google import genai
import sys

def main(prompt):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=prompt
        )
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Please provide exactly one prompt argument")
        sys.exit(1)

    prompt = sys.argv[1].strip()
    if not prompt:
        print("Error: Prompt cannot be empty")
        sys.exit(1)

    main(prompt)
    
