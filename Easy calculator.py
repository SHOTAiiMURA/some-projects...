
#def of add
def adding(int1, int2):
    return int1 + int2
#def of sub
def subtract(int1, int2):
    return int1 - int2
#def of multiply
def multiply(int1, int2):
    return int1 * int2
#def of divide
def divide(int1, int2):
    if int2 != 0:
        return int1 / int2
    else:
        print("cannot divided by 0")

#main defenition of cal and say "welcome to python calculator"
def main_calculator():
    print("Welcome to Python Calculator")

#let user input number
    num_user_1 = float(input("Enter 1st number: "))
    num_user_2 =float(input("Enter 2nd number: "))

    print("1, adding")
    print("2, subtract")
    print("3, multiply")
    print("4, divide")
#let user to choose what calculation want to execute.
    choose_option_user = input("Please choose one of execution: ")
#use if function to execute calculation.
    if choose_option_user == "1":
        num_results =  adding(num_user_1, num_user_2)
    elif choose_option_user == "2":
        num_results = subtract(num_user_1, num_user_2)
    elif choose_option_user == "3":
        num_results = multiply(num_user_1, num_user_2)
    elif choose_option_user == "4":
        num_results = divide(num_user_1, num_user_2)
    else:
        print("invalid action")

#print the results
    print("Number is", num_results)

    return num_results


# 計算機を実行
if __name__=="__main__":
    main_calculator()


