import os

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        details = lambda it: (
                            p := os.path.join(target_dir, it),
                            f"- {it}: file_size={os.path.getsize(p)} bytes, is_dir={os.path.isdir(p)}"
                        )[1]
        content = os.listdir(target_dir)
        return "\n".join(list(map(details, content)))
    except Exception as e:
        return f"Error: {e}"