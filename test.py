arr = ["1 2", "3 4"]
result = dict(map(lambda pair: map(int, pair.split()), arr))
print(result)
