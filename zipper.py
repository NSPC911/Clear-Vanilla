import os
import zipfile
import time

output_dir = '.'
repo_path = os.getcwd()
repo_name = os.path.basename(repo_path)
output_path = os.path.join(output_dir, f"{repo_name}.mcpack")
start_time = time.time()
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_path):
        if '.git' in dirs:
            dirs.remove('.git')
        if '.gitattributes' in files:
            files.remove('.gitattributes')
        if 'zipper.py' in files:
            files.remove('zipper.py')
        if f"{repo_name}.mcpack" in files:
            files.remove(f"{repo_name}.mcpack")
        if os.path.abspath(__file__) in files:
            files.remove(os.path.abspath(__file__))
        for file in files:
            file_path = os.path.join(root, file)
            file_path_length = len(file_path)
            print(f"\rArchiving: {file_path}{' ' * (os.get_terminal_size().columns - file_path_length - 12)}", end='', flush=True)
            zipf.write(file_path, os.path.relpath(file_path, repo_path))
elapsed_time = time.time() - start_time
print(f"\nRepository zipped successfully at {output_path}")
print(f"Elapsed Time: {elapsed_time:.2f} seconds")
