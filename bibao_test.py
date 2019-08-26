def counter(first=0):
    a = first

    def add_one():
        nonlocal a
        a += 1
        return a
    return add_one


num1 = counter(1)
print(num1())
print(num1())
