import pandas as pd
from pathlib import Path


REPORT_FILE = "outputs/evaluation_report.csv"


def save_report(
    session_id,
    image_name,
    question,
    answer,
    feedback
):

    Path("outputs").mkdir(
        exist_ok=True
    )

    data = {
        "session_id": [session_id],
        "image_name": [image_name],
        "question": [question],
        "answer": [answer],
        "feedback": [feedback]
    }

    df = pd.DataFrame(data)

    if Path(REPORT_FILE).exists():

        df.to_csv(
            REPORT_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        df.to_csv(
            REPORT_FILE,
            index=False
        )