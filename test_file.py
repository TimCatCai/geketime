# file = open("name.txt", 'w')
# file.write(u"刘备")
# file.close()
#
# file1 = open("name.txt")
# print(file1.read())
# file1.close()
#
# file2 = open("name.txt", 'a')
# file2.write(u"诸葛亮")
# file2.close()

file3 = open("name.txt")
for line in file3.readlines():
    print(line, end="")

print(file3.tell())
# 跳转到固定位置，相对于开头来说
file3.seek(1)

# 第一参数为偏移量，第二个 0 为文件开头，1从当前位置偏移，2从文件末尾
file3.seek(5, 0)
print(file3.tell())

file3.close()
