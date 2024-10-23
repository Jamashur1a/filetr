import random
import time

def Get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number")

array_size = Get_int("Enter array size: ")
print("Creating random array...")

list_of_nums = [i for i in range(array_size)]
random.shuffle(list_of_nums)

def merge_sort(array):
    array_length = len(array)

    if array_length <= 1:
        return array
    
    middle_index = array_length // 2
    left_side_of_array = merge_sort(array[:middle_index])
    right_side_of_array = merge_sort(array[middle_index:])

    return merge(
        left=left_side_of_array,
        right=right_side_of_array
    )

def merge(left, right):
    return_array = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            return_array.append(left[left_index])
            left_index += 1
        else:
            return_array.append(right[right_index])
            right_index += 1
    
    # Logic to merge remaining parts of arrays if there are equal numbers or due to size differences
    return_array.extend(left[left_index:])
    return_array.extend(right[right_index:])

    return return_array

print("Sorting...")
start = time.time()
sorted_list = merge_sort(list_of_nums)

end = time.time()

print(f"Original list: {list_of_nums}")
print(f"Sorted list: {sorted_list}")
print(f"Time: {end - start}")
