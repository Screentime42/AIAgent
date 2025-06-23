import os

def get_files_info(working_directory, directory=None):
   working_directory = os.path.abspath(working_directory)
   joined_path = os.path.join(working_directory, directory)
   target_directory = os.path.abspath(joined_path)

   if not os.path.isdir(target_directory):
      return f"Error: '{directory}' is not a directory"
   
   if not target_directory.startswith(working_directory):
      return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

   try:
      directory_contents = os.listdir(target_directory)

      result = []

      for file in directory_contents:
         full_path = os.path.join(target_directory, file)
         size = os.path.getsize(full_path)
         is_dir = os.path.isdir(full_path)
         result.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")
   except Exception as e:
      return f"Error: {e}"

   
   final_result = "\n".join(result)
   return final_result