import os
import zipfile
import time
import json
import uuid

repo_path = str(os.getcwd())[:-2]
output_path = os.path.join(repo_path, "pack.mcpack")
start_time = time.time()
with open(f"{repo_path}manifest.json","r") as manifest:
    manifestr = json.loads(manifest.read())
    manifestr["header"]["uuid"] = str(uuid.uuid4())
    manifestr["modules"][0]["uuid"] = str(uuid.uuid4())
with open(f"{repo_path}manifest.json","w") as manifest:
    manifest.write(json.dumps(manifestr,indent=4))
total_files = sum(len(files) for _, _, files in os.walk(repo_path))
processed_files = 0
with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_path):
        if ".git" in dirs:
            dirs.remove(".git")
        if "py" in dirs:
            dirs.remove("py")
        if "README.md" in files:
            files.remove("README.md")
        if ".gitattributes" in files:
            files.remove(".gitattributes")
        if "zipper.py" in files:
            files.remove("zipper.py")
        if "pack.mcpack" in files:
            files.remove("pack.mcpack")
        for file in files:
            file_path = os.path.join(root, file)
            file_path_length = len(file_path)
            processed_files += 1
            percentage = (100*processed_files)//total_files
            try:
                print(f'\r{percentage}% Archiving: {file_path}{" " * (os.get_terminal_size().columns - file_path_length - 15 - len(str(percentage)))}', end="", flush=True)
            except OSError:
                print(f"\r{percentage} Archiving: {file_path}", end="", flush=True)
            zipf.write(file_path, os.path.relpath(file_path, repo_path))
elapsed_time = time.time() - start_time
print(" " * os.get_terminal_size().columns)
print(f"Repository zipped successfully at {output_path}")
print(f"Elapsed Time: {elapsed_time:.2f} seconds")
