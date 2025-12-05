import random

print("=== Treasure Adventure! ===")
print("Find the hidden treasure in a 5 x 5 map!")

treasure_x = random.randint(1, 5)
treasure_y = random.randint(1, 5)

while True:
    try:
        x = int(input("Guess the X coordinate (1-5): "))
        y = int(input("Guess the Y coordinate (1-5): "))
    except ValueError:
        print("Please enter a number!")
        continue

    if x < 1 or x > 5 or y < 1 or y > 5:
        print("Out of the map! Try again.")
        continue

    if x == treasure_x and y == treasure_y:
        print("🎉 You found the treasure! Congratulations! 🎉")
        break
    else:
        distance = abs(x - treasure_x) + abs(y - treasure_y)
        print(f"No treasure here! Hint:

