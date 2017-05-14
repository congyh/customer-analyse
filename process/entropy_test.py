test = [(1000, 5.234112412), (1001, 2.2312312), (1002, 7.31234123)]
# for i in range(len(test)):
#     test[i] = round(test[i], 3)

print(test)

entropy_max = max(test, key=lambda item: item[1])
print("entropy_max:", entropy_max)
print("index of entropy_max:", test.index(entropy_max))
test[test.index(entropy_max)] = (None, 0)
print(test)

entropy_max = max(test, key=lambda item: item[1])
print("entropy_max:", entropy_max)
print("index of entropy_max:", test.index(entropy_max))
test[test.index(entropy_max)] = (None, 0)
print(test)

entropy_max = max(test, key=lambda item: item[1])
print("entropy_max:", entropy_max)
print("index of entropy_max:", test.index(entropy_max))
test[test.index(entropy_max)] = (None, 0)
print(test)
