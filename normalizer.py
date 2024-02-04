import pandas as pd
import os
import typo_finder

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
        return s

    # remap char to the layout
    if s in mappings[layout]:
        return mappings[layout][s]

    return s


def get_duration(data):
    start, end = map(float, data[5:7])
    return end - start


def amend_record(correct_str, typing_record, record):
    typed_str = "".join([a for a, b in typing_record])

    for src, dst, size in typo_finder.get_matching_strs(typed_str, correct_str):
        # print(src, dst, size)

        for i in range(size):
            record[typing_record[src + i][1]][2] = correct_str[dst + i]
            # print(record[typing_record[src + i][1]])


def convert_typing_session(session_file, layout="qwerty"):
    with open(session_file) as file:
        lines = [l.split("\t") for l in file]
        record = []
        correct = True

        def helper(text_pt, line_num, record_i):
            nonlocal record, layout, lines, correct
            correct_string = lines[0][2]
            curr_string = []
            duration_residue = 0

            while line_num < len(lines):
                data = lines[line_num]
                duration = get_duration(data)
                char = string_norm(data[-2], layout)

                try:
                    correct_char = string_norm(correct_string[text_pt], layout)
                except:
                    # line overflowed, so we need to backspace more
                    return False

                # backspaces are inconsistent in some files and can either represent one or more backspaces
                if char == "BKSP":
                    duration_residue += duration

                    if (
                        line_num < len(lines) - 1
                        and string_norm(lines[line_num + 1][-2], layout) == "BKSP"
                    ):
                        # remove lines of duplicate backspaces
                        duration_residue += get_duration(lines[line_num + 1])
                        lines = lines[: line_num + 1] + lines[line_num + 2 :]
                        text_pt -= 1
                        continue
                    else:
                        line_num += 1

                        # check currently typed string against ideal string[ptr] for matching elements and only update between last back space and current
                        # Recursively check any number of back spaces going back to the start
                        amend_record(correct_string[:text_pt], curr_string, record)
                        passed = False

                        for i in range(text_pt):
                            text_pt -= 1
                            # print("curr string!")
                            # print(curr_string)
                            passed = helper(text_pt, line_num, record_i)

                            # check, should this be + 1?
                            record = record[:record_i]

                            if passed:
                                break
                        if passed:
                            return True
                    record.append(["BKSP", duration, correct_char])
                    record_i += 1
                    continue
                else:
                    line_num += 1

                    # we have to treat shift and caps lock special, because they add time onto the following character's typing time, but should not be included in key set
                    # this does pose a problem with caps KEY caps KEY tho... since the latter is undoing the former... annoying of people who type that way lol
                    if len(char) > 1:  # (char == "SHIFT") or (char == "CAPS_LOCK"):
                        if char not in ("SHIFT", "CAPS_LOCK", "ARW_LEFT", "ARW_RIGHT"):
                            print(char)
                            print(1 / 0)
                        duration_residue += duration
                        continue
                    else:
                        duration += duration_residue
                        duration_residue = 0
                        text_pt += 1

                record.append([char, duration, correct_char])
                curr_string.append((char, record_i))
                correct &= char == correct_char
                record_i += 1

            # Successfully made it through all lines without overflow
            amend_record(correct_string, curr_string, record)

            if "But thank you for the offer" in correct_string:
                print(record)
                print(1 / 0)
            return True

        helper(0, 0, 0)


# convert_typing_session(f"files/{participant}/10.txt")

participants = pd.read_csv("metadata_participants.txt", sep="\t")

for i, p in participants[participants["AVG_WPM_15"] > 1].iterrows():
    ID = p["PARTICIPANT_ID"]
    layout = p["LAYOUT"]
    participant_dir = "files/" + str(ID).zfill(6)

    for file in os.listdir(participant_dir):
        print(participant_dir + "/" + file)
        convert_typing_session(
            participant_dir + "/" + file,
            layout,
        )
