def sum(a, b:int, c=0) -> int: # 函数返回 int 值 
	# a, b的类型为int, c的默认值为 0 
    return a+b, a-b  # 多返回值, 元组形式返回

num    = sum(10, 5)  # num=(15, 5)元组
print(num)
num, _ = sum(10, 5)  # num=15
print(num)
