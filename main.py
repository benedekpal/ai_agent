import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from prompts import system_prompt

from prompts import system_prompt
from call_function import call_function, available_functions

from config import MAX_ITERATIONS


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

    for i in range(MAX_ITERATIONS):
        try:
            # there is only a return value if not response.function_calls
            # so if there is a function call the loop won't break
            response = generate_content(client, messages, verbose)
            if response:
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
    
    if response:
        print("Final response:")
        print(response)
    else:
        print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
        sys.exit(1)


def generate_content(client, messages, verbose):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], 
                                               system_instruction=system_prompt),
        )

        function_responses = []

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.candidates:
            for candidate in response.candidates:
                #print("====================================")
                #print("candidate", candidate)
                #print("\n")
                #print("candidate.content", candidate.content)
                #print("====================================")

                #messages is a list and by appending to it we also modify the value of it in the main
                function_call_content = candidate.content
                messages.append(function_call_content)

        if not response.function_calls:
            return response.text

        if response.function_calls:

            for func_call in response.function_calls:
                function_call_result = call_function(func_call, verbose)

                if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                    raise Exception("empty function call result")
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("no function responses generated, exiting.")

            messages.append(types.Content(role="tool", parts=function_responses))

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
    
