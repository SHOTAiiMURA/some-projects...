import random

#generate rancom number
random_num = random.randint(1, 10)

#let user to input number
user_name = input("Please tell me your name: ")
print("greate"+user_name+"guess number wihin 5 attemps")
guess_attempt = 0
#guess if user`s number are high or low , 5 attempts
while guess_attempt < 5:
    guess = int(input())
    guess_attempt += 1

#if number is low generate sentence
    if guess > random_num:
        print("your guess number is greater")
    elif guess < random_num:
        print("your guess numer is lower")
    else:
        break

#if it correnct, genrate sentence
if guess == random_num:
    print("congrats," + user_name+"!" ,"your guess is correct" , user_name , "guessed number" , str(random_num))
else:
    print("sorry" , user_name , "you failed to guess my number" , str(random_num) , "was guess number")

