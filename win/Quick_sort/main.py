import random

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number")

array_size = get_int("Enter the size of the array: ")
print("Creating random array...")

nums = [i for i in range(array_size)]
random.shuffle(nums)

def quick_sort(arr):
    length = len(arr)

    if length <= 1:
        return arr

    right_idx = 0
    left_idx = -1
    pivot_idx = length - 1

    while right_idx <= pivot_idx:
        if arr[right_idx] < arr[pivot_idx]:
            left_idx += 1
            
            temp = arr[left_idx]
            arr[left_idx] = arr[right_idx]
            arr[right_idx] = temp

        right_idx += 1
    
    temp = arr[left_idx + 1]
    arr[left_idx + 1] = arr[pivot_idx]
    arr[pivot_idx] = temp

    return_list = quick_sort(arr[:left_idx + 1]) + [arr[left_idx + 1]] + quick_sort(arr[left_idx + 2:])
    return return_list

print(nums)
print("-------------------")
sorted_output = quick_sort(nums)
print(sorted_output)
