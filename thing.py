import typo_finder

text = """there are 
some 3rrors in my text
but I cannot find them"""


"""def fuzzy_search(search_key, text, strictness):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            similarity = diff.SequenceMatcher(None, word, search_key)
            if similarity.ratio() > strictness:
                return " '{}' matches: '{}' in line {}".format(search_key, word, i + 1)


print(fuzzy_search("errors", text, 0.8))"""

print(
    typo_finder.SequenceMatcher(
        None, "But thak you for the offer", "But thank you for the offer"
    ).get_matching_blocks()
)
