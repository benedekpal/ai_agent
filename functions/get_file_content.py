import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    if file_path:
        target_file = os.path.abspath(os.path.join(target_dir, file_path))

        print("target_file", target_file)
        print("target_dir", target_dir)

    if not target_file.startswith(target_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)

        is_too_long = len(file_content_string) > MAX_CHARS
        file_content_string = file_content_string[:MAX_CHARS]

        if is_too_long:
            file_content_string += f"\n ...File \"{file_path}\" truncated at 10000 character"

        return file_content_string
    
    except Exception as e:
        return f"Error: {e}"