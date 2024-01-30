import pandas as pd
import os

participants = pd.read_csv("metadata_participants.txt", sep="\t")

ids = participants["PARTICIPANT_ID"]

for ID in participants["PARTICIPANT_ID"]:
    participant_file_name = "files/" + str(ID).zfill(6)

    if not os.path.exists(participant_file_name + ".txt"):
        print(participant_file_name + ".txt", "does not exist")
        continue

    print(participant_file_name + ".txt")
    test_data = pd.read_csv(participant_file_name + ".txt", sep="\t", quoting=3)

    # make a folder to session files in
    if not os.path.exists(participant_file_name):
        os.makedirs(participant_file_name)

    session_id = ""
    session_file = None

    with open(participant_file_name + ".txt") as file:
        # skip header
        file.readline()

        for l in file:
            data = l.split("\t")

            # make a new file for each session
            if session_id != data[1]:
                session_id = data[1]
                session_file = open(f"{participant_file_name}/{session_id}.txt", "w")

            # super jank fix because they included tabs as a data point :face_palm:
            if len(data) > 10:
                data = data[:8] + ["Tab"] + data[-1]

            session_file.write("\t".join(data))

    print(1 / 0)
    """for section_id in test_data["TEST_SECTION_ID"].unique():
        section = test_data[(test_data["TEST_SECTION_ID"] == section_id)]

        section.to_csv(
            participant_file_name + f"/{section_id}.txt", sep="\t", index=False
        )"""
