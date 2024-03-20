import time
#slicing = creating a substring by extracting elements from another string.
#   indexing[] or slice()

#name = "Bro Code"

#first_name = name[0:3]
#last_name = name[4:]
#reverse_name = name[::-1]
#rint(reverse_name)

# website="http://google.com"
# website2="http://wikipedia.com"
# slice =slice(7,-4)
#
# print(website[slice])
# print(website2[slice])
#
# #logical operators (and, or, not)
# temp = int(input("what is the temperatureoutside?: "))
#
# if temp >= 0 and temp <= 30:
#     print("tempreture is good today")
#     print("go outside")
#
#
#
# for i in range(10, 100,2):
#     print(i)

#loop control statements = change a loops wxcution from its normal sequence

# while True:
#     name = input("Enter you name: ")
#     if name != "":
#         break

# phone_number = "123-123-123"
# for i in phone_number:
#     if i == "-":
#         continue
#     print(i,end="")

# for i in range(1,21):
#     if i == 13:
#         pass
#     else:
#         print(i, end="")

#lsit = used to store multiple items in a single variable.

# food = ["pizza","hambuger","hotdog","apple"]
# food[0]="sushi"
# print(food[0:])

#2D lists = a list of lsits

# drinks = ["coffee","sody","tea"]
# dinner=["pizza","buger","hotgod"]
# desert =["cake","ice cream"]
#
# food = [drinks, dinner, desert]
# print(food[1][2])

#tuple = collection which is ordered and unchangeable
#          used to group together related data

# student =("bro",21,"male")
# print(student.count("bro"))
# print(student.index("male"))
#
# for i in student:
#     print(i)
#
# if "bro"in student:
#     print("Bro is here!")

#dictionary = store unique key: value pairs
#           fast since they use hashing, allow us to access a value quickly

# capitals = {"usa":"new york",
#             "india":"new dehli",
#             "Japan":"Tokyo",
#             "France":"paris"}
# #print(capitals["Japan"])
# #print(capitals.get("Germany"))
# #print(capitals.keys())
# #print(capitals.values())
#
# capitals.update({"Germany":"Beriln"})
# print(capitals.items())

#index oeprator [] = gives access to a sequence element (str, list, tuples)

#name = "bro code!"

# if(name[0].islower()):
#     name = name.capitalize()
#
# print(name)
# first_name=name[0:4].upper()
# last_name = name[4:].upper()
# last_charater = name[-1]
# print(first_name)
# print(last_name)
# print(last_charater)

#function = a block of code which is executed only when it is called.
# def hello(name,named):
#     print("Hello!"+name+named)
#
# hello("Bro","code"  )

#return statement = function send python values/objects bakc to the caller.
#                   these calues are know as the functions return value.

# def multiply(number1, number2):
#     result = number1 * number2
#     return result
# x = multiply(8,8)
# print(x)

#keyword arguments

#for loop

# for i in range(50,100,2):
#     print(i+2)
#
# for seconds in range(10,0, -1):
#     print(seconds)
#     time.sleep(1)
# print("Happy new year")

#nested loop = the inner loop will finish all of it's iterations before.

rows = int(input("enter rows: "))
colums = int(input("enter rows: "))
symbol = input("Enter a symbol to use: ")

for i in range(rows):
    for j in range(colums):
        print(symbol, end="")
    print()




