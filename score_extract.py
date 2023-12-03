import pandas as pd
from pathlib import Path


def properties_name(df: pd.DataFrame):
    columns = list(df.columns)
    result = []
    for column in columns:
        if "unnamed" in column.lower():
            continue
        result.append(column)
    return result


def clean_data_frame(df: pd.DataFrame):
    properties = properties_name(df)
    columns = ["Unnamed: 1"]
    for i in range(1, len(df.columns)):
        if "Unnamed" in df.columns[i]:
            continue
        columns.append(df.columns[i + 2])
    for c in df.columns:
        if c not in columns:
            df = df.drop([c], axis=1)
    df = df.drop([0], axis=0)
    df = df.fillna(0)

    new_columns = dict()
    for i in range(len(properties)):
        new_columns[columns[i]] = properties[i]
    df.rename(columns=new_columns, inplace=True)
    return df


def extract_score(xlsx_path) -> pd.DataFrame:
    df = pd.read_excel(xlsx_path)
    df = clean_data_frame(df)

    return df


def get_students_list(student_number_path: Path):
    students = pd.read_csv(student_number_path)
    student_list = []
    students["student_number"] = students["student_number"].astype(str)
    for i in range(len(students["student_number"])):
        student_list.append(str(students["student_number"][i]))
    return student_list, students
