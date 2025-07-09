import json
import os
import PIL.Image
import PIL

def get_root() -> str:
    default_path: str = os.getcwd()

    if default_path.endswith("code"):
        default_path = default_path[:-4]

    return default_path

def read_file(file_path: str) -> list[str]:
    current_file = open(file_path, "r")

    return_data: list[str] = []

    for line in current_file:
        return_data.append(sanitise_line(line))
    
    return return_data

def sanitise_line(line_data: str) -> str:
    return line_data.replace("\n", "").replace("ï»¿", "")

def write_file(file_path: str, file_contents: str) -> None:
    current_file = open(file_path, "w")
    current_file.write(file_contents)
    current_file.close()

def append_file(file_path: str, append_contents: str) -> None:
    current_file = open(file_path, "a")
    current_file.write(f"\n{append_contents}")
    current_file.close()

def write_json_file(file_path: str, file_contents: dict) -> None:
    json_file = open(file_path, "w")
    json.dump(file_contents, json_file)

def read_json_file(file_path: str) -> dict:
    with open(file_path) as json_file:
        file_data: dict = json.load(json_file)

    try:
        return file_data[0]
    except:
        return file_data

def relocate_file(old_path: str, new_path: str) -> None:
    file_contents: list[str] = read_file(old_path)
    # delete_file(old_path)
    write_file(new_path, file_contents)

def copy_file(old_path: str, new_path: str) -> None:
    file_contents = open(old_path, "r")
    # delete_file(old_path)
    write_file(new_path, file_contents)

def copy_image_file(old_path: str, new_path: str) -> None:
    print(old_path)
    print(new_path)
    old_image = PIL.Image.open(old_path)
    new_image = old_image.save(new_path)

def relocate_json_file(old_path: str, new_path: str) -> None:
    file_contents: dict = read_json_file(old_path)
    delete_file(old_path)
    write_json_file(new_path, file_contents)

def delete_file(file_path: str) -> None:
    os.remove(file_path)

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def get_files_in_folder(folder_path: str, extension: str) -> list[str]:
    return_files: list[str] = []

    folder = os.walk(folder_path)

    for (root, directories, files) in folder:
        for file in files:
            if extension.lower() in file.lower():
                return_files.append(file)

    return return_files

def file_in_folder(folder_path: str, file_path: str, extensions: list[str]) -> bool:
    files: list[str] = []
    files_in_folder: list[str]

    for i in range(len(extensions)):
        files_in_folder = get_files_in_folder(folder_path, extensions[i])

        files.extend(files_in_folder)

    if file_path in files: return True
    else: return False