# 调整栈大小
import sys
sys.setrecursionlimit(100000)  # 设置栈大小为10000


# 阿克曼函数

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

# 用户输入
m = int(input("请输入m的值："))
n = int(input("请输入n的值："))

# 调用函数并打印结果
result = ackermann(m, n)
print(f"Ackermann函数的结果为：{result}")
