import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    if file_path:
        target_file = os.path.abspath(os.path.join(target_dir, file_path))

    if not target_file.startswith(target_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'

    if ".py" not in file_path:
        f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", target_file],
            capture_output=True,
            text=True,
            cwd=target_dir,
            timeout=30
        )
        output_parts = []
        if result.stdout.strip():
            output_parts.append("STDOUT: " + result.stdout.strip())
        if result.stderr.strip():
            output_parts.append("STDERR: " + result.stderr.strip())
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        return "\n".join(output_parts) if output_parts else "No output produced."
    
    except Exception as e:
        return f"Error: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Calls a python function located in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)