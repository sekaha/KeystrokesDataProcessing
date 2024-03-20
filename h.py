import time
from itertools import product

gram_length = 3
chars = "abcdefghijklmnopqrstuvwxyz"
swaps = ["a", "b"]

start_time = time.time()
perm = ["" for _ in range(gram_length - 1)]
count = 0


def helper(swap, chars, d, offset):
    global count
    d -= 1

    if d < 0:
        # Where I would process the delta
        res = perm[:offset] + [swap] + perm[offset:]
        print(res)
        count += 1
        return
    else:
        if d < offset:
            chars = chars.replace(swap, "")

        for c in chars:
            perm[d] = c
            helper(swap, chars, d, offset)


new_chars = chars

for swap in swaps:
    for offset in range(gram_length):
        print("offset", offset)
        helper(swap, new_chars, gram_length - 1, offset)
    new_chars = new_chars.replace(swap, "")

end_time = time.time()
print(end_time - start_time)

print(count)

start_time = time.time()

new = set(
    [
        combo
        for swap in swaps
        for combo in product(chars, repeat=gram_length)
        if swap in combo
    ]
)
end_time = time.time()
print(end_time - start_time)

print(len(new))
