import time
import random

#Insertion Sort
#Time Complexity: O(n^2)
#Space Complexity: O(1)

size = 10

list_of_nums = [i for i in range(0,size)]
random.shuffle(list_of_nums)

print(f"Original list: {list_of_nums}")

start = time.time()

for i in range(1,size):
    for x in range(i,0,-1):
        holder = list_of_nums[x]
        behined_holder = list_of_nums[x -1]

        if behined_holder > holder:
            list_of_nums[x] = behined_holder
            list_of_nums[x -1] = holder
        elif behined_holder < holder:
            break

end = time.time()

print(f"Sorted list: {list_of_nums}")    
print(f"Function took {end - start} seconds")
