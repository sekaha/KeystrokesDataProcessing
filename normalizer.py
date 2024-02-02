import pandas as pd
import os

# Layout Mappings, ['qwerty' 'azerty' 'qwertz' 'dvorak']
qwerty = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>? "


def get_mapping(keys):
    return {k: v for k, v in zip(keys, qwerty)}


mappings = {
    "azerty": get_mapping(
        "`1234567890-=azertyuiop[]\\qsdfghjkl;'wxcvbnm,./~!@#$%^&*()_+AWERTYUIOP{}|QSDFGHJKL:\"WXCVBNM<>? "
    ),
    "dvorak": get_mapping(
        "`1234567890[]',.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz~1234567890{}\"<>PYFGCRL?+|AOEUIDHTNS_:QJKXBMWVZ "
    ),
    "qwerty": get_mapping(qwerty),
    "qwertz": get_mapping(
        "`1234567890ß´qwertzuiopü+#asdfghjklöäyxcvbnm,.-~!\"§$%&/()=?`QWERTZUIOPÜ*'ASDFGHJKLÖÄYXCVBNM;_ "
    ),  # the dataset is frankly not very descriptive of how this should look, so I based it off https://kbdlayout.info/KBDGR?arrangement=ANSI104
}

participant = "000005"
shifted_keys = 'QWERTYUIOPASDFGHJKLZXCVBNM,.<>?:"{}~!@\#$%^&*()_+|'


def string_norm(s, layout):
    if len(s) > 1:
        return s.title()

    # remap char to the layout
    if s in mappings[layout]:
        return mappings[layout][s]

    return s


def convert_typing_session(session_file, layout="qwerty"):
    with open(session_file) as file:
        lines = [l.split("\t") for l in file]
        record = []

        def helper(text_pt, line_num, record_i):
            nonlocal record, layout, lines
            duration_residue = 0

            while line_num < len(lines):
                data = lines[line_num]
                start, end = map(float, data[5:7])
                duration = end - start
                correct_string = data[2]
                char = string_norm(data[-2], layout)

                # We have to treat shift special, since it's a precursor to a correct character but isn't represented in the typing test string of course
                if char == "Bksp":
                    # print(lines[line_num - 1])
                    duration_residue += duration

                    if (
                        line_num < len(lines) - 1
                        and string_norm(lines[line_num + 1][-2], layout) == "Bksp"
                    ):
                        lines = lines[: line_num + 1] + lines[line_num + 2 :]
                        text_pt -= 1
                        continue
                    else:
                        line_num += 1

                        # Recursively check any number of back spaces
                        for i in range(text_pt):
                            record = record[:record_i]
                            text_pt -= 1

                            if helper(text_pt, line_num, record_i):
                                break
                    continue
                else:
                    line_num += 1
                    try:
                        correct_char = string_norm(correct_string[text_pt], layout)
                    except:
                        return False

                    if (char == "Shift") or (char == "Caps_Lock"):
                        duration_residue += duration
                        continue
                    else:
                        duration += duration_residue
                        duration_residue = 0
                        text_pt += 1

                record.append((char, duration, correct_char))
                record_i = record_i + 1

            # Successfully made it through all lines without overflow
            return True

        helper(0, 0, 1)

        for l in record:
            print(l)


convert_typing_session(f"files/{participant}/10.txt")

participants = pd.read_csv("metadata_participants.txt", sep="\t")

for ID in participants["PARTICIPANT_ID"]:
    participant_dir = "files/" + str(ID).zfill(6)

    for file in os.listdir(participant_dir):
        print(participant_dir + "/" + file)
        convert_typing_session(participant_dir + "/" + file)
