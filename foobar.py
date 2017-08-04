"""Just using this so it looks nice"""
import sys

if __name__ == "__main__":
    for i in range(0, 101):
        sys.stdout.write(" ")
        if i%3 == 0 and i%5 == 0:
            sys.stdout.write("foobar")
        elif i%3 == 0:
            sys.stdout.write("foo")
        elif i%5 == 0:
            sys.stdout.write("bar")
        else:
            sys.stdout.write(str(i))
        sys.stdout.write(",")
