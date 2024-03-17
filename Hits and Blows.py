import random
#４つのランダムな数字を出力する
def generated_random_num()
random_4_digit = random.sample(range(10),4)
print(random_4_digit)
#プレイヤーからの入力を受け取る。

def main_his_and_blow():
    user_random_num = input("Please input random 4 digit number: ")

#入力された数字の正当性をチェックする（数字の重複や桁数など）。
    if user_random_num == random_4_digit:
        print("please select diffrent number again")

    elif user_random_num
        print("invalid number, please type different nunber: ")

main_his_and_blow()
#プレイヤーの入力と正解を比較し、ヒット（数字と位置が一致する）とブロー（数字は一致するが位置が異なる）を数える。


#ヒットが3つになるまで推測を繰り返す。


#ヒットが3つになったらゲームを終了する。