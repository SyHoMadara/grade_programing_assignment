import shutil
import moss
import score_extract
import os
from pathlib import Path
import pandas as pd
import code_collecting

TEMP_DIR = Path(f"{os.getcwd()}").resolve() / ".tmp"
code_collecting.mkdir(TEMP_DIR, True)

ROW_CODE_EXTRACTION_PATH = TEMP_DIR / "code_extraction"
CODES_PATH = Path("./zip_file").resolve()
DETECT_COPY_DIR = TEMP_DIR / "detect_copys"
SERISE = []
RESULT_SHEET_PATH = Path("./scores.xlsx").resolve()


code_collecting.extract_all_zips(CODES_PATH, ROW_CODE_EXTRACTION_PATH)
for dir in os.listdir(ROW_CODE_EXTRACTION_PATH):
    SERISE.append(dir)


code_collecting.collect_all_code_of_questions(
    ROW_CODE_EXTRACTION_PATH, DETECT_COPY_DIR, "c"
)

STUDENT_PATH = Path("./students.csv").resolve()
students, student_df = score_extract.get_students_list(STUDENT_PATH)


SCORE_SHETES_PATH = Path("./score_sheets").resolve()

scores = []
for serie_name in os.listdir(SCORE_SHETES_PATH):
    scores.append(
        [
            score_extract.extract_score(SCORE_SHETES_PATH / serie_name),
            serie_name.split("_")[1],
        ]
    )


# detect copy
for i in range(len(SERISE)):
    serise_index = -1
    for j in range(len(scores)):
        if scores[j][1] == SERISE[i].split("_")[1]:
            serise_index = j
            break
    for question in os.listdir(DETECT_COPY_DIR / SERISE[i]):
        shammer_students = moss.get_all_copys(DETECT_COPY_DIR / SERISE[i] / question)
        print(f"Copy of question {question} detected.")
        scores[serise_index][0].loc[
            scores[serise_index][0]["مشخصات کاربر"].isin(shammer_students),
            "سوال " + question,
        ] = 0
    scores[serise_index][0].rename(
        columns={"مشخصات کاربر": "student_number"}, inplace=True
    )
    scores[serise_index][0] = pd.merge(
        student_df, scores[serise_index][0], on="student_number", how="inner"
    )
    scores[serise_index][0].fillna(0, inplace=True)
    print(f"Serise {scores[serise_index][1]} was checked.")
print("All files were checked")


print("Saving...")
with pd.ExcelWriter("score_result.xlsx") as writer:
    for i in range(len(scores)):
        scores[i][0].to_excel(writer, sheet_name=scores[i][1])
print("All scores were saved.")

shutil.rmtree(TEMP_DIR, ignore_errors=True)