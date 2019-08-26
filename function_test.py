from functools import reduce
# name = open("name.txt")
# # 将读取的所有数据去掉换行符
# # data = name.read().replace('\n', '|').split('|')
# # 一行一行的读，并精简每一行的开头空格和回车符号
# result = []
# for line in name.readlines():
#     temp_file.mp3 = line.strip().strip('\n').split('|')
#     # for i in range(len(temp_file.mp3)):
#     #     temp_file.mp3[i] = temp_file.mp3[i].strip()
#     # 使用map实现相同功能
#     temp_file.mp3 = list(map(lambda x: x.strip(), temp_file.mp3))
#     result += temp_file.mp3
# print(result)
#
# # 迭代器
#
# aList = [1, 2, 3, 4]
# it = iter(aList)
# for i in it:
#     print(i)
#
# # 生成器
#
#
# def frange(start, end, step):
#     while start < end:
#         yield start
#         start += step
#
#
# for i in frange(1, 10, 0.5):
#     print(i)
#

print(reduce(lambda x, y: x*y, [1, 2.5, 3], 1))

print(list(filter(lambda x: x > 2, [1, 2, 5, 34])))

print(list(zip([1, 2, 4], [4])))

