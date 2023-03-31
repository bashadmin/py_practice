import random
import time

def sequential_search(lst, x):
    start_time = time.time()
    for i in range(len(lst)):
        if lst[i] == x:
            end_time = time.time()
            return (i, end_time-start_time)
    end_time = time.time()
    return (None, end_time-start_time)

def ordered_sequential_search(lst, x):
    start_time = time.time()
    for i in range(len(lst)):
        if lst[i] == x:
            end_time = time.time()
            return (i, end_time-start_time)
        elif lst[i] > x:
            end_time = time.time()
            return (None, end_time-start_time)
    end_time = time.time()
    return (None, end_time-start_time)

def binary_search_iterative(lst, x):
    start_time = time.time()
    low = 0
    high = len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == x:
            end_time = time.time()
            return (mid, end_time-start_time)
        elif lst[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    end_time = time.time()
    return (None, end_time-start_time)

def binary_search_recursive(lst, x, low=0, high=None):
    start_time = time.time()
    if high is None:
        high = len(lst) - 1
    if low > high:
        end_time = time.time()
        return (None, end_time-start_time)
    mid = (low + high) // 2
    if lst[mid] == x:
        end_time = time.time()
        return (mid, end_time-start_time)
    elif lst[mid] < x:
        return binary_search_recursive(lst, x, mid + 1, high)
    else:
        return binary_search_recursive(lst, x, low, mid - 1)


def main():
    sizes = [500, 1000, 10000]
    search_functions = [sequential_search, ordered_sequential_search, binary_search_iterative, binary_search_recursive]
    x = -1 # element to search for in worst case scenario

    for size in sizes:
        print(f"\nSize: {size}")
        for search_function in search_functions:
            total_time = 0
            for i in range(100):
                lst = sorted(random.sample(range(1, size*10), size))
                _, time_taken = search_function(lst, x)
                total_time += time