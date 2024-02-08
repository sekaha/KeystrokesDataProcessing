import pandas as pd
import re
import os

### Layout Mapping ###
qwerty = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>? "
shifted_keys = 'QWERTYUIOPASDFGHJKLZXCVBNM,.<>?:"{}~!@\#$%^&*()_+|'


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


def string_norm(s, layout):
    if len(s) > 1:
        return s

    # remap char to the layout
    if s in mappings[layout]:
        return mappings[layout][s]

    return s


#### Typo Finder ####
# Build an index mapping elements of sequence_b to their indices
def build_index(sequence_b):
    # Construct a dictionary where keys are elements of sequence_b and values are lists of their indices in sequence_b
    element_to_indices = {}

    for index, element in enumerate(sequence_b):
        indices = element_to_indices.setdefault(element, [])
        indices.append(index)

    return element_to_indices


# Find the longest matching str between two slices of the sequences
def find_longest_match(
    sequence_a, sequence_b, element_to_indices, start_a, end_a, start_b, end_b
):
    # Initialize variables to track the best matching str
    best_start_a, best_start_b, best_size = start_a, start_b, 0
    j_to_length = {}
    empty_list = []

    # Iterate over elements in sequence a to find the longest matching str
    for i in range(start_a, end_a):
        get_j_to_length = j_to_length.get
        new_j_to_length = {}

        for j in element_to_indices.get(sequence_a[i], empty_list):
            if j < start_b:
                continue

            if j >= end_b:
                break

            length = new_j_to_length[j] = get_j_to_length(j - 1, 0) + 1

            # Update the best matching str if a longer one is found
            if length > best_size:
                best_start_a, best_start_b, best_size = (
                    i - length + 1,
                    j - length + 1,
                    length,
                )

        j_to_length = new_j_to_length

    # Extend the matching str with junk elements if applicable
    while (
        best_start_a > start_a
        and best_start_b > start_b
        and sequence_a[best_start_a - 1] == sequence_b[best_start_b - 1]
    ):
        best_start_a, best_start_b, best_size = (
            best_start_a - 1,
            best_start_b - 1,
            best_size + 1,
        )

    while (
        best_start_a + best_size < end_a
        and best_start_b + best_size < end_b
        and sequence_a[best_start_a + best_size] == sequence_b[best_start_b + best_size]
    ):
        best_size += 1

    # Return the Match tuple representing the longest matching str
    return (best_start_a, best_start_b, best_size)


# Get list of matching strs between sequences
def get_matching_strs(str_a, str_b):
    # Maintain a queue of the upper and lower bounds of the str a and the str b
    len_a, len_b = len(str_a), len(str_b)
    queue = [(0, len_a, 0, len_b)]
    matching_strs = []

    element_to_indices = build_index(str_b)

    # Loop until the queue is empty, finding matching strs
    while queue:
        start_a, end_a, start_b, end_b = queue.pop()
        i, j, size = x = find_longest_match(
            str_a, str_b, element_to_indices, start_a, end_a, start_b, end_b
        )

        # Add the matching str to the list
        if size:
            matching_strs.append(x)

            # Add new subregions to the queue for further examination
            if start_a < i and start_b < j:
                queue.append((start_a, i, start_b, j))

            if i + size < end_a and j + size < end_b:
                queue.append((i + size, end_a, j + size, end_b))

    # Sort the matching strs and merge adjacent strs
    matching_strs.sort()
    prev_start_a = prev_start_b = prev_size = 0
    non_adjacent = []

    for cur_start_a, cur_start_b, cur_size in matching_strs:
        if (
            prev_start_a + prev_size == cur_start_a
            and prev_start_b + prev_size == cur_start_b
        ):
            prev_size += cur_size
        else:
            if prev_size:
                non_adjacent.append((prev_start_a, prev_start_b, prev_size))

            prev_start_a, prev_start_b, prev_size = cur_start_a, cur_start_b, cur_size

    if prev_size:
        non_adjacent.append((prev_start_a, prev_start_b, prev_size))

    return [tuple(item) for item in non_adjacent]


### Processing and Writing the Output ####
def get_duration(data):
    start, end = map(float, data[5:7])
    return end - start


def amend_record(correct_str, typing_record, record, threshold=1):
    typed_str = "".join([a for a, b in typing_record])
    correct = 0

    for src, dst, size in get_matching_strs(typed_str, correct_str):
        # print(src, dst, size)
        if size > threshold:
            correct += size

            for i in range(size):
                record[typing_record[src + i][1]][2] = True

    return correct


def convert_typing_session(session_file, wpm_file, layout="qwerty"):
    correct_chars_typed = 0
    lines = [l.split("\t") for l in file]
    record = []
    line_num = record_i = 0
    correct_string = lines[0][2]
    curr_string = []

    # the times can be huge and require floats, but the duration is fine as an int
    total_duration = int(float(lines[-1][5]) - float(lines[0][5]))
    print("duration", total_duration)
    # duration_residue = 0

    while line_num < len(lines):
        data = lines[line_num]
        # duration = get_duration(data)
        char = string_norm(data[-2], layout)

        # backspaces are inconsistent in some files and can either represent one or more backspaces
        if len(char) > 1:
            line_num += 1

            if (
                char == "SHIFT"
                and (line_num < len(lines))
                and string_norm(lines[line_num][-2], layout) in shifted_keys
            ):
                # duration_residue += duration
                continue

            correct_chars_typed += amend_record(correct_string, curr_string, record)
            curr_string = []
            record.append([char, data[5], False])
            record_i += 1
            continue
        else:
            line_num += 1
            # duration += duration_residue
            # duration_residue = 0

        record.append([char, data[5], False])
        curr_string.append((char, record_i))
        record_i += 1

    # Successfully made it through all lines without overflow

    # Write the processed session file
    prefix = re.match(r"(.*)\.txt", session_file.name).group(1)
    print(f"{prefix}_processed.txt")
    new_file = open(f"{prefix}_processed.txt", "w")
    new_file.write("\n".join([", ".join([str(x) for x in l]) for l in record]))

    # add the WPM for this session to the meta data file
    correct_chars_typed += amend_record(correct_string, curr_string, record)
    wpm = round((correct_chars_typed / 5) / (total_duration / 60000))
    print("wpm", wpm)
    session_name = prefix.split("/")[-1]
    wpm_file.write(f"{session_name} {wpm}\n")


### Bringing it all together baby :))
participants = pd.read_csv("metadata_participants.txt", sep="\t")

# participants["AVG_WPM_15"] > 0
with open("wpm_metadata.txt", "w") as wpm_record:
    with open("files/517947/5579566.txt") as file:
        convert_typing_session(file, wpm_record)

    """
    for i, p in participants.iterrows():
        ID = p["PARTICIPANT_ID"]
        layout = p["LAYOUT"]ee
        participant_dir = "files/" + str(ID).zfill(6)

        for file_name in os.listdir(participant_dir):
            if re.match(r"(.*)\.txt", file_name).group(1).isdigit():
                print(participant_dir + "/" + file_name)

                with open(participant_dir + "/" + file_name) as file:
                    convert_typing_session(file, wpm_record, layout)
    """
e
