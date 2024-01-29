import pandas as pd

participants = pd.read_csv("files/metadata_participants.txt", sep="\t")

# print(participants["LAYOUT"].unique())
# print(participants[((participants["AVG_WPM_15"] >= 0))])
# print(
#    participants[((participants["AVG_WPM_15"] >= 100))][
#        (participants["FINGERS"] == "9-10")
#    ]
# )

# print(
#     participants[((participants["AVG_WPM_15"] > 90))][
#         (participants["FINGERS"] == "9-10")
#     ]
# )
#
# print(participants["PARTICIPANT_ID"])

for ID in participants["PARTICIPANT_ID"]:
    with open("files/" + f"{100000+ID}_keystrokes.txt") as file:
        print()
