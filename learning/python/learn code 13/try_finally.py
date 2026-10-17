# try:
#     a= int|(input("hey,enter a number:"))
#     print(a)
# except Exception as e:
#     print(e)
# finally:
#     print("hey I am inside of finally")

# main()


def main():
    try:
        a = int(input("Hey, enter a number: "))
        print(a)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Hey, I am inside the finally block")

main()
