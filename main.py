import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the file's contents and prints the max_chars of the content if over the max_chars limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that has the content that needs to be obtained.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the specified python file and returns relative output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that is required.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates and writes string to a file, if the file does not exist. If the file does exist, overwrites the file with the given string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that is required."),
            "content": types.Schema(
               type=types.Type.STRING,
               description="The string that is to be the contents of the file"
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose == True:
      print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
      print(f" - Calling function: {function_call_part.name}")

    function_map = {
       "get_files_info": get_files_info,
       "get_file_content": get_file_content,
       "run_python_file": run_python_file,
       "write_file": write_file
    }
   
    if function_call_part.name in function_map:
        function = function_map[function_call_part.name]
        args = dict(function_call_part.args)  # copy the dict, don't mutate the original
        args["working_directory"] = "./calculator"
        result = function(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    
def main():
   system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

   verbose = '--verbose' in sys.argv
   
   prompt_parts = [arg for arg in sys.argv[1:] if arg != '--verbose']
   prompt = ' '.join(prompt_parts)

   messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
   ]

   response = client.models.generate_content(
      model='gemini-2.0-flash-001', 
      contents=messages,
      config=types.GenerateContentConfig(
         tools=[available_functions],
         system_instruction=system_prompt
         )
   )

   if len(sys.argv) < 2:
      print("Error: No prompt provided")
      sys.exit(1)

   if verbose:
      print(f'User prompt: "{prompt}"')
      print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
      print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


   if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, verbose=verbose)
            # Try to access the response directly
            try:
                result = function_call_result.parts[0].function_response.response
            except AttributeError:
                raise Exception("Fatal Error: Missing 'response' attribute in function tool result")
            if verbose:
                print(f"-> {result}")
            return result
        
        
   else:
      print(response.text)

if __name__ == "__main__":
    main()

