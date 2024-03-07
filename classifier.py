from math import atan2, degrees


class keyboard:
    def __init__(self):
        self.row_offsets = [-0.25, 0, 0.5]

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

    def get_pos(self, k):
        return self.key_to_pos[k]

    def get_col(self, k):
        return self.key_to_pos[k][0]

    def get_finger(self, k):
        return self.x_to_finger[self.key_to_pos[k][0]]

    def get_row(self, k):
        return self.key_to_pos[k][1]

    def get_hand(self, k):
        return abs(self.key_to_pos[k][0]) / self.key_to_pos[k][0]


kb = keyboard()


def same_col(bg):
    return kb.get_col(bg[0]) == kb.get_col(bg[1])


def same_hand(bg):
    return kb.get_hand(bg[0]) == kb.get_hand(bg[1])


def inwards_rotation(bg):
    if same_hand(bg):
        if abs(kb.get_col(bg[0])) < abs(kb.get_col(bg[1])):
            outer, inner = bg[1], bg[0]
        elif abs(kb.get_col(bg[0])) > abs(kb.get_col(bg[1])):
            outer, inner = bg[0], bg[1]
        else:
            return False

        if kb.get_row(outer) > kb.get_row(inner):
            return True

    return False


def get_rotation(bg):
    outer, inner = bg[1], bg[0]

    if same_hand(bg):
        if abs(kb.get_col(bg[0])) < abs(kb.get_col(bg[1])):
            outer, inner = bg[1], bg[0]
        elif abs(kb.get_col(bg[0])) > abs(kb.get_col(bg[1])):
            outer, inner = bg[0], bg[1]
        else:
            return None

        x1, y1 = kb.get_pos(outer)
        x2, y2 = kb.get_pos(inner)

        return round(
            degrees(
                atan2(
                    (y1 - y2),
                    ((x1 + kb.row_offsets[3 - y1]) - (x2 + kb.row_offsets[3 - y2]))
                    * kb.get_hand(bg[0]),
                )
            )
        )

    return None


def outwards_rotation(bg):
    if same_hand(bg):
        if abs(kb.get_col(bg[0])) < abs(kb.get_col(bg[1])):
            outer, inner = bg[1], bg[0]
        elif abs(kb.get_col(bg[0])) > abs(kb.get_col(bg[1])):
            outer, inner = bg[0], bg[1]
        else:
            return False

        if kb.get_row(outer) < kb.get_row(inner):
            return True

    return False


def is_adjacent(bg):
    return abs(kb.get_col(bg[0]) - kb.get_col(bg[1])) == 1


def get_dx(bg):
    x1, y1 = kb.get_pos(bg[0])
    x2, y2 = kb.get_pos(bg[1])

    return abs((x1 + kb.row_offsets[3 - y1]) - (x2 + kb.row_offsets[3 - y2]))


def get_dy(bg):
    return abs(kb.get_row(bg[0]) - kb.get_row(bg[1]))


def get_distance(bg, ex):
    return ((get_dx(bg)) ** ex + (get_dy(bg)) ** ex) ** 0.5


def is_scissor(bg):
    return (
        get_dy(bg) == 2
        and not same_finger(bg)
        and kb.get_hand(bg[0]) == kb.get_hand(bg[1])
    )  # get_dx(bg) < 2 and get_dy(bg) == 2 and not same_finger(bg)


def same_finger(bg):
    return bg[0] != bg[1] and kb.get_finger(bg[0]) == kb.get_finger(bg[1])


def test():
    # scissor: with row stagger is < 2 x_dist
    print(get_dx("so"))
    print("left hand")
    print("bq", ":", get_rotation("bq"))
    print("bw", ":", get_rotation("bw"))
    print("be", ":", get_rotation("be"))
    print("br", ":", get_rotation("br"))
    print()
    print("zw", ":", get_rotation("zw"))
    print("ze", ":", get_rotation("ze"))
    print("zr", ":", get_rotation("zr"))
    print("zt", ":", get_rotation("zt"))
    print()
    print("cq", ":", get_rotation("cq"))
    print("cw", ":", get_rotation("cw"))
    print("cr", ":", get_rotation("cr"))
    print("ct", ":", get_rotation("ct"))
    print()
    print("right hand")
    print("np", ":", get_rotation("np"))
    print("no", ":", get_rotation("no"))
    print("ni", ":", get_rotation("ni"))
    print("nu", ":", get_rotation("nu"))
    print()
    print("/o", ":", get_rotation("/o"))
    print("/i", ":", get_rotation("/i"))
    print("/u", ":", get_rotation("/u"))
    print("/y", ":", get_rotation("/y"))
    print()
    print(",p", ":", get_rotation(",p"))
    print(",o", ":", get_rotation(",o"))
    print(",u", ":", get_rotation(",u"))
    print(",y", ":", get_rotation(",y"))
