import random

print("=== 寶物大冒險！===")
print("你在一個 5 x 5 的地圖中，要找到隱藏的寶物！")

treasure_x = random.randint(1, 5)
treasure_y = random.randint(1, 5)

while True:
    try:
        x = int(input("請猜寶物的 X 座標 (1-5): "))
        y = int(input("請猜寶物的 Y 座標 (1-5): "))
    except ValueError:
        print("請輸入數字！")
        continue

    if x < 1 or x > 5 or y < 1 or y > 5:
        print("超出地圖範圍！再試一次～")
        continue

    if x == treasure_x and y == treasure_y:
        print("🎉你找到寶物了！恭喜通關！🎉")
        break
    else:


