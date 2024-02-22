"""


print(kb_dict)"""


class keyboard:
    def __init__(self):
        self.x_to_finger = {
            5: "lp",
            4: "lr",
            3: "lm",
            2: "li",
            1: "li",
            -1: "ri",
            -2: "ri",
            -3: "rm",
            -4: "rr",
            -5: "rp",
        }

        kb = ["qwertyuiop", "asdfghjkl;", "zxcvbnm,./"]
        self.key_to_pos = {}

        for y, row in enumerate(kb):
            for x, c in enumerate(row):
                new_x = x - 5 if x < 5 else x - 4

                self.key_to_pos[c] = (new_x, 3 - y)

        self.pos_to_key = dict(zip(self.key_to_pos.values(), self.key_to_pos.keys()))
        print(self.pos_to_key)

    def get_pos(self, k):
        return self.key_to_pos[k]

    def get_col(self, k):
        return self.key_to_pos[k][0]

    def get_finger(self, k):
        return self.x_to_finger[self.key_to_pos[k][0]]

    def get_row(self, k):
        return self.key_to_pos[k][1]


kb = keyboard()


def same_col(bg):
    return kb.get_col(bg[0]) == kb.get_col(bg[1])


def same_finger(bg):
    return kb.get_finger(bg[0]) == kb.get_finger(bg[1])


print(same_col("aq"))
print(same_col("sq"))
print(same_col("fr"))
print(same_finger("rb"))
print(same_finger("fg"))
print(same_finger("yi"))
