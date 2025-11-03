def find_peak_element(arr, left=None, right=None):
    # для первого вызова функции
    if left is None and right is None:
        left, right = 0, len(arr) - 1

    # базовый случай
    if left == right:
        return arr[left]

    mid = (left + right) // 2

    # проверяем пиковый элемент
    left_neighbor = arr[mid - 1] if mid > 0 else float('-inf')
    right_neighbor = arr[mid + 1] if mid < len(arr) - 1 else float('-inf')

    # если текущий элемент больше или равен соседним, возвращаем его как пиковый
    if arr[mid] >= left_neighbor and arr[mid] >= right_neighbor:
        return arr[mid]

    # применяем рекурсивно функцию на левую половину, если левый сосед больше текущего элемента
    if left_neighbor > arr[mid]:
        return find_peak_element(arr, left, mid - 1)
    # иначе, на правую половину
    else:
        return find_peak_element(arr, mid + 1, right)


n = int(input())
arr = list(map(int, input().split()))
print(find_peak_element(arr))
