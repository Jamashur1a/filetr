import time

size = 100000000
list_of_nums = [i for i in range(0, size, 3)]
goal = list_of_nums[-1]


start = time.time()

low, high = 0, len(list_of_nums) - 1
attempt_guess = list_of_nums[(low + high) // 2]

while low <= high:
    mid = (low + high) // 2
    attempt_guess = list_of_nums[mid]

    if attempt_guess == goal:
        break

    if attempt_guess > goal:
        high = mid - 1
    else:
        low = mid + 1

end = time.time()

if attempt_guess == goal:
    print(f"Found {goal} at index {mid}")
else:
    print(f"{goal} not found")
    
print(f"Function took {end - start} seconds")
