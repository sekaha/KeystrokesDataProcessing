from itertools import product

print(
    len(
        [
            combo
            for swap in "ab"
            for combo in product("qwertyuiopasdfghjkl;zxcvbnm,./", repeat=2)
            if swap in combo
        ]
    )
)


print(
    len(
        set(
            [
                combo
                for swap in "ab"
                for combo in product("qwertyuiopasdfghjkl;zxcvbnm,./", repeat=2)
                if swap in combo
            ]
        )
    )
)
