k = int(input())
count = [0] * 10
for _ in range(4):
    row = input().strip()
    for ch in row:
        if ch.isdigit():
            count[int(ch)] += 1

score = 0
for t in range(1, 10):
    if 0 < count[t] <= 2 * k:
        score += 1

print(score)