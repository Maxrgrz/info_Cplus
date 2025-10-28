import random
import time
import multiprocessing as mp
import numpy as np
import heapq


def partition(arr, left, right):
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quicksort(arr):
    def _quicksort(arr, left, right):
        if left < right:
            pivot = partition(arr, left, right)
            _quicksort(arr, left, pivot - 1)
            _quicksort(arr, pivot + 1, right)

    arr_copy = arr[:]
    _quicksort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def merge_sorted_arrays(arrays):
    return list(heapq.merge(*arrays))


def parallel_quicksort(arr, num_processes):
    if num_processes <= 1 or len(arr) < 10000:
        return quicksort(arr)

    chunk_size = len(arr) // num_processes
    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_processes)]
    if len(arr) % num_processes != 0:
        chunks[-1].extend(arr[num_processes * chunk_size:])

    with mp.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(quicksort, chunks)

    return merge_sorted_arrays(sorted_chunks)


def generate_random_array(size):
    return [random.randint(1, 1000000) for _ in range(size)]


def measure_time(sort_func, arr, num_processes = None, runs = 3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        if num_processes:
            sort_func(arr, num_processes)
        else:
            sort_func(arr)
        times.append(time.perf_counter() - start)
    return np.mean(times)


def calculate_speedup(seq_time, par_time):
    return seq_time / par_time if par_time > 0 else 0


def run_tests():
    sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
    thread_counts = [1, 2, 4, 8]
    results = []

    for size in sizes:
        arr = [random.randint(0, 100000) for _ in range(size)]
        seq_time = measure_time(parallel_quicksort, arr.copy(), 1)

        parallel_times = []
        for threads in thread_counts[1:]:
            time_taken = measure_time(parallel_quicksort, arr.copy(), threads)
            parallel_times.append(time_taken)

        speedups = [calculate_speedup(seq_time, pt) for pt in parallel_times]

        results.append({
            'size': size,
            'sequential_time': seq_time,
            'parallel_times': parallel_times,
            'speedups': speedups
        })

    return results, thread_counts


def print_results(results, thread_counts):
    print("\nРезультаты тестирования многопоточной быстрой сортировки")
    header = "Размер массива | Последовательная (1 поток) |"
    header += "".join([f" {t} потоков |" for t in thread_counts[1:]])
    header += " " + " | ".join([f"Speedup ({t})" for t in thread_counts[1:]]) + " |"
    print(header)
    print("-" * len(header))

    for res in results:
        row = f"{res['size']:>12} | {res['sequential_time']:>25.6f} |"
        row += "".join([f" {t:>10.6f} |" for t in res['parallel_times']])
        row += "".join([f" {s:>10.2f} |" for s in res['speedups']])
        print(row)


if __name__ == "__main__":
    print("Запуск тестов многопоточной быстрой сортировки...")
    results, thread_counts = run_tests()
    print_results(results, thread_counts)