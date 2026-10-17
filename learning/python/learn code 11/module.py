# def myfunc():
#     print("hello world!")
#     myfunc()
#     print(__name__)
#     if _name_=="__main__":
#      print("we are directly running this code")


def myfunc():
    print("Hello, world!")

if __name__ == "__main__":
    myfunc()
    print(__name__)
    print("We are directly running this code")
