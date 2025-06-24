import os

def write_file(working_directory, file_path, content):
   working_directory = os.path.abspath(working_directory)
   joined_path = os.path.join(working_directory, file_path)
   target_path = os.path.abspath(joined_path)

   if not target_path.startswith(working_directory):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
   
   try:
      parent_dir = os.path.dirname(target_path)
      os.makedirs(parent_dir, exist_ok=True)

      with open(target_path, "w") as f:
         f.write(content)

      return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


   except Exception as e:
      return f"Error: {e}"