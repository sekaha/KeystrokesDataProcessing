import pandas as pd
import re
import os
from multiprocessing import Process, Manager

session_wpms = dict(
    map(
        lambda x: map(int, x.split()),
        [l for l in open("wpm_metadata.txt")],
    ),
)

DATA_TYPES = {
    "bistrokes": (2, 0),
    # "tristrokes": (3, 0),
    # "quadristroke": (4, 0),
    # "1-skip": (2, 1),
    # "2-skip": (2, 2),
    # "3-skip": (2, 3),
    # "4-skip": (2, 4),
    # "5-skip": (2, 5),
    # "6-skip": (2, 6),
    # "7-skip": (2, 7)
}

valid_chars = set("-qwertyuiopasdfghjkl'zxcvbnm,._QWERTYUIOPASDFGHJKL\"ZXCVBNM<>")


def split_lines(file):
    # Function to split lines in a file
    with open(file) as f:
        lines = [l.strip("\n").split(", ") for l in f]
    return lines


def process_window(file, size, skip, strokes):
    lines = split_lines(file)
    print(file)

    # Function to process the window of lines
    for i in range(len(lines) - size - skip + 1):
        window = lines[i : i + size + skip]

        # check correctness of string, only correct strings will get accepted
        if all([l[2] == "True" for l in window]):
            stroke_data = window[: int(size / 2)] + window[-int(size / 2 + 0.5) :]
            duration = int(float(stroke_data[-1][1]) - float(stroke_data[0][1]))
            stroke = "".join([l[0] for l in stroke_data])

            if all([c in valid_chars for c in stroke]):
                strokes[stroke] = strokes.get(stroke, []) + [duration]


def process_data_type(alias, size, skip, wpm, shared_strokes):
    strokes = shared_strokes[alias]
    participants = pd.read_csv("metadata_participants.txt", sep="\t")
    processes = []

    for i, p in participants.iterrows():
        ID = p["PARTICIPANT_ID"]
        participant_dir = "typingrecords/" + str(ID).zfill(6)

        for file_name in os.listdir(participant_dir):
            match = re.match(r"(.*)_processed\.txt", file_name)

            if (
                match
                and match.group(1).isdigit()
                and session_wpms[int(match.group(1))] > wpm
            ):
                print(session_wpms[int(match.group(1))])
                p = Process(
                    target=process_window,
                    args=(participant_dir + "/" + file_name, size, skip, strokes),
                )
                processes.append(p)
                p.start()

    for p in processes:
        p.join()

    with open(f"nstrokes/{alias}_{wpm}.txt", "w") as output:
        for k in sorted(strokes.keys()):
            output.write(k + ", " + ", ".join(map(str, sorted(strokes[k]))) + "\n")

    print("nstrokes/" + alias + ".txt")


def get_strokes(wpm):
    manager = Manager()
    shared_strokes = {alias: manager.dict() for alias in DATA_TYPES.keys()}
    processes = []

    for alias, (size, skip) in DATA_TYPES.items():
        p = Process(
            target=process_data_type, args=(alias, size, skip, wpm, shared_strokes)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


get_strokes(0)
