# try and except
try:
    #answer=10/0
    user_num=int(input("Please enter a number: "))
    print(user_num)

except ZeroDivisionError as err:
    print(err)

except ValueError:
    print("invalid number")


