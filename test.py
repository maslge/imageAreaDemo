#!/usr/bin/python3

# from  https://www.programiz.com/python-programming/closure
# https://docs.python-guide.org/writing/structure/


def star(func):
    def inner(*args, **kwargs):
        print("*" * 30)
        func(*args, **kwargs)
        print("*" * 30)
    return inner


def percent(func):
    def inner(*args, **kwargs):
        print("%" * 30)
        func(*args, **kwargs)
        print("%" * 30)
    return inner


# @star
# @percent
def printer(msg):
    print(msg)


star(percent(printer))("hello")
value = 4 * 80
print(value)


# printer("Hello")
