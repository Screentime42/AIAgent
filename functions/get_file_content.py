import os

def get_file_content(working_directory, file_path):
   working_directory = os.path.abspath(working_directory)
   joined_path = os.path.join(working_directory, file_path)
   target_path = os.path.abspath(joined_path)

   if not target_path.startswith(working_directory):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
   
   if not os.path.isfile(target_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
   
   max_chars = 10000
      
   try:
      with open(target_path, "r") as f:
         content = f.read()

      if len(content) > max_chars:
         truncated = content[:max_chars]
         return f'{truncated} [...File "{file_path}" truncated at {max_chars} characters]'
      else:
         return content
   
   except Exception as e:
      return f"Error: {e}"