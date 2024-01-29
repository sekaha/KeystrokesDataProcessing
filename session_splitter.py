import pandas as pd
import os

participants = pd.read_csv("metadata_participants.txt", sep="\t")

ids = participants["PARTICIPANT_ID"]

for ID in participants["PARTICIPANT_ID"]:
    participant_file_name = "files/" + str(ID).zfill(6)
    print(participant_file_name)

    with open(participant_file_name + ".txt") as file:
        test_data = pd.read_csv(file, sep="\t")

        # make a folder to session files in
        if not os.path.exists(participant_file_name):
            os.makedirs(participant_file_name)

        for section_id in test_data["TEST_SECTION_ID"].unique():
            section = test_data[(test_data["TEST_SECTION_ID"] == section_id)]

            section.to_csv(
                participant_file_name + f"/{section_id}.txt", sep="\t", index=False
            )
