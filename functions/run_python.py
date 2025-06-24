import os
import subprocess

def run_python_file(working_directory, file_path):
   working_directory = os.path.abspath(working_directory)
   joined_path = os.path.join(working_directory, file_path)
   target_path = os.path.abspath(joined_path)

   if not target_path.startswith(working_directory):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
   
   if not os.path.exists(target_path):
      return f'Error: File "{file_path}" not found.'
   
   if not file_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file.'
   

   try:
      result = subprocess.run(
         ["python3", target_path],
         capture_output=True,
         text=True,
         cwd=working_directory,
         timeout=30
      )

      
      output_lines = []
      if result.stdout:
         output_lines.append(f"STDOUT:\n{result.stdout.strip()}")
      if result.stderr:
         output_lines.append(f"STDERR:\n{result.stderr.strip()}")
      if result.returncode != 0:
         output_lines.append(f"Process exited with code {result.returncode}")
      if not output_lines:
         return "No output produced."

      return "\n".join(output_lines)

   except subprocess.TimeoutExpired:
      return "Error: Process timed out after 30 seconds."
   except Exception as e:
      return f"Error: {e}"
