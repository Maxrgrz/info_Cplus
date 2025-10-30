def find_peak_element(arr):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        # проверка на пиковый элемент
        left_neighbor = arr[mid - 1] if mid > 0 else float('-inf')
        right_neighbor = arr[mid + 1] if mid < len(arr) - 1 else float('-inf')

        if arr[mid] >= left_neighbor and arr[mid] >= right_neighbor:
            return arr[mid]

        # переход в левую половину, если левый сосед больше
        elif left_neighbor > arr[mid]:
            right = mid - 1
        # иначе - правая половина
        else:
            left = mid + 1

    return arr[left]


n = int(input())
arr = list(map(int, input().split()))
print(find_peak_element(arr))
