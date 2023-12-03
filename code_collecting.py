import os
from pathlib import Path
import shutil
import zipfile


def seperate_file_name(file_name):
    file_name, file_extension = os.path.splitext(os.path.basename(file_name))
    return file_name, file_extension


def finde_file(dir: Path, suffix):
    files = []
    for file in os.listdir(dir):
        _, ext = seperate_file_name(dir / file)
        if ext == suffix:
            files.append(file)
    return files


def mkdir(path: Path, delete_if_exist: bool):
    if delete_if_exist and os.path.exists(path):
        # print(f"{str(path)} exist do you want delete it? [y/n]")
        # if input().lower() == "y":
        #     shutil.rmtree(path)
        # else:
        #     raise Exception(f"{path} exist")
        shutil.rmtree(path)
    elif not os.path.exists(path):
        os.makedirs(path)


def extract_all_zips(zips_path: Path, dist_path: Path):
    mkdir(dist_path, True)
    for file in finde_file(zips_path, ".zip"):
        file_name, _ = seperate_file_name(file)
        os.makedirs(dist_path / file_name)
        try:
            with zipfile.ZipFile(zips_path / file, "r") as zip_ref:
                zip_ref.extractall(dist_path / file_name)
        except Exception as ex:
            print(ex)


def merge_codes(code_dir: Path, merged_path: Path, language, student: list = []):
    mkdir(merged_path, True)
    for serise_folder in os.listdir(code_dir):
        mkdir(merged_path / serise_folder, True)
        for student_folder in os.listdir(code_dir / serise_folder):
            if (
                len(student) != 0
                and student_folder.strip().replace(" ", "") not in student
            ):
                continue
            integrated_code = f"//{student_folder}\n"
            for question_folder in os.listdir(
                code_dir / serise_folder / student_folder
            ):
                cfiles = finde_file(
                    code_dir / serise_folder / student_folder / question_folder,
                    f".{language}",
                )
                integrated_code += f"//{question_folder}\n"
                for ccode in cfiles:
                    integrated_code += f"//{ccode}\n\n"
                    with open(
                        code_dir
                        / serise_folder
                        / student_folder
                        / question_folder
                        / ccode,
                        "r",
                    ) as f:
                        integrated_code += f.read()
                    integrated_code += "\n\n"
            int_file_name = f"{merged_path}/{serise_folder}/{student_folder.strip().replace(' ', '')}.{language}"
            with open(int_file_name, "w") as f:
                f.write(integrated_code)


def collect_all_code_of_questions(code_dir: Path, dist_path: Path, languege):
    mkdir(dist_path, True)
    for serise_folder in os.listdir(code_dir):
        mkdir(dist_path / serise_folder, True)
        for student_folder in os.listdir(code_dir / serise_folder):
            for question_folder in os.listdir(
                code_dir / serise_folder / student_folder
            ):
                mkdir(dist_path / serise_folder / question_folder, False)
                cfiles = finde_file(
                    code_dir / serise_folder / student_folder / question_folder,
                    f".{languege}",
                )
                for ccode in cfiles:
                    shutil.copyfile(
                        code_dir
                        / serise_folder
                        / student_folder
                        / question_folder
                        / ccode,
                        dist_path
                        / serise_folder
                        / question_folder
                        / f"{student_folder.strip().replace(' ', '')}_{ccode}",
                    )
