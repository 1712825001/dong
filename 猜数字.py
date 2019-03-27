import random

secret = random.randint(1,10000)
temp = input("猜一个数: ")
guess = int(temp)

while guess != secret:
    if guess > secret:
        print("大了")
    else:
        print("小了")

    temp = input("猜错啦，请重新输入吧: ")
    guess = int(temp)
    if guess == secret:
        print("正确")
        print("猜对了也没有奖励!")
print("游戏结束")
