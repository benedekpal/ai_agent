import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


def main(user_prompt, verbose):
    print("verbose", verbose)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(user_prompt)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], 
                                               system_instruction=system_prompt),
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.function_calls:
            function_calls = response.function_calls.copy()
            for func_call in function_calls:
                print(f"Calling function: {func_call.name}({func_call.args})")
        else:
            print("Response:")
            print(response.text)

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)
    
if __name__ == "__main__":

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    main(args, verbose)
    
