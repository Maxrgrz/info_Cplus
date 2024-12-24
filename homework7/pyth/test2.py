from ctypes import *
summer = CDLL('./arrayDll.dll')

arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
arr1_ctype = (c_int * len(arr1))(*arr1)
arr2_ctype = (c_int * len(arr1))(*arr2)

summer.sumArrays.argtypes = [POINTER(c_int), POINTER(c_int), c_int]
summer.sumArrays.restype = POINTER(c_int)
sumArraysPY = summer.sumArrays(arr1_ctype, arr2_ctype, len(arr1))

res = [sumArraysPY[i] for i in range(len(arr1))]
print(res)
