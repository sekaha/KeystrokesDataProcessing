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


# Test cases
def test():
    test_cases = [
        ("But thak you for the offer", "But thank you for the offer"),
        ("abcde", "xyzabcuvw"),
        ("apple banana orange", "orange apple banana"),
        ("abcdefg", "gfedcba"),
        ("", "test"),
        ("test", ""),
        ("", ""),
        ("1234567890", "0987654321"),
        ("This is a test", "This is another test"),
        ("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"),
        ("abababababababab", "babababababababa"),
        ("AAAAAAA", "AAA"),
        ("AAA", "AAAAAAA"),
        ("abc", "abc"),
        ("abc", "def"),
        ("abc", "abcd"),
        ("abcd", "abc"),
        (
            "I will bring the pillow back tomorrow and get with you then.",
            "I will bring the pillow back tomorrow an dget with you then.",
        ),
    ]

    # Test the functionality
    for str_a, str_b in test_cases:
        matching_strs = get_matching_strs(str_a, str_b)
        print(f"Matching strs for '{str_a}' and '{str_b}': {matching_strs}")
