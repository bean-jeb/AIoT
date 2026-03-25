# LED 하나씩 제어하기 위해 LED 클래스 불러오기
from gpiozero import LED
from time import sleep

# GPIO 핀 번호 변수로 정의
carLedRed = 2
carLedYellow = 3
carLedGreen = 4
humanLedRed = 20
humanLedGreen = 21

# 각 LED를 객체로 생성 (해당 핀에 연결된 LED 제어 가능)
carLedRed = LED(2)
carLedYellow = LED(3)
carLedGreen = LED(4)
humanLedRed = LED(20)
humanLedGreen = LED(21)

try:
    while 1:
        # 차량: 초록불 / 사람: 빨간불
        carLedRed.value = 0
        carLedYellow.value = 0
        carLedGreen.value = 1
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(3.0)

        # 차량: 노란불 / 사람: 빨간불 유지
        carLedRed.value = 0
        carLedYellow.value = 1
        carLedGreen.value = 0
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(1.0)

        # 차량: 빨간불 / 사람: 초록불
        carLedRed.value = 1
        carLedYellow.value = 0
        carLedGreen.value = 0
        humanLedRed.value = 0
        humanLedGreen.value = 1
        sleep(3.0)

except KeyboardInterrupt:
    pass

# 종료 시 모든 LED 끄기
carLedRed.value = 0
carLedYellow.value = 0
carLedGreen.value = 0
humanLedRed.value = 0
humanLedGreen.value = 0
