import math

odds = [3.1, 2.9, 4]
float = sum(1/x for x in odds)

print(float, str(round((1-float) * 100, 2)) + "%")