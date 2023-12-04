import os
from pathlib import Path
import urllib.request
from bs4 import BeautifulSoup


def correct_path(path: Path):
    p = str(path)
    p = p.replace(" ", "\\ ")
    return p


def get_moss_response(files_path: Path, max_m=10, file_type="c"):
    if max_m < 3:
        raise Exception("max_m can not be less than 3")
    # print(f"moss -l {file_type} -m {max_m} {correct_path(files_path)}/*.{file_type}")
    res = os.popen(
        f"moss -l {file_type} -m {max_m} {correct_path(files_path)}/*.{file_type}"
    ).read()
    res = res.splitlines()
    if not res[1] == "OK":
        return None
    print(f"Serise {files_path} uploaded")
    return res[-1]


def percent(file_name):
    res = file_name.split(" ")[-1]
    res = res[1:-2]
    return int(res)


def extract_student_number(file_path: str):
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    student_number = name.split("_")[0]
    return str(student_number)


def get_all_copys(
    file_path: Path, trash_hold_percent: int = 70, max_m: int = 10, file_type: str = "c"
):
    url_res = get_moss_response(file_path, max_m, file_type)
    fp = urllib.request.urlopen(url_res)
    mybytes = fp.read()
    print("requst to moss was seccused.")
    mystr = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(mystr, "html.parser")
    res = set()
    for i in soup.find_all("a"):
        if f".{file_type}" not in i.text:
            continue
        if percent(i.text) >= trash_hold_percent:
            res.add(extract_student_number(i.text.split()[0]))
    return res
