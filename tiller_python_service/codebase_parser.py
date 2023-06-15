import pathlib

CODE_EXTENSIONS = [".py", ".rs"]


def parse(path):
    for file_path in path.rglob(f"*[{'|'.join(CODE_EXTENSIONS)}]"):
        if file_path.is_file() and "__" not in str(file_path):
            with open(file_path, "r") as f:
                yield f.read()
