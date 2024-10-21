n = int(input())  # the number of temperatures to analyse
positives, negatives = [], []
result = 0

for i in input().split():
    # t: a temperature expressed as an integer ranging from -273 to 5526
    t = int(i)
    if t > 0:
        positives.append(t)
    elif t < 0:
        negatives.append(t)

if positives == [] and negatives == []:
    result = 0
else:
    if positives == []:
        result = max(negatives)
    elif negatives == []:
        result = min(positives)
    elif min(positives) <= abs(min(negatives)):
        result = min(positives)
    elif min(positives) > abs(min(negatives)):
        result = max(negatives)

print(result)
