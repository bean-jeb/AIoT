# 라이브러리에서 여러 LED를 한 번에 다루기 위한 LEDBoard 불러오기
from gpiozero import LEDBoard
# 시간 지연을 위한 sleep 함수 불러오기
from time import sleep

# GPIO 핀 2,3,4,20,21에 연결된 LED들을 하나의 묶음으로 생성
leds = LEDBoard(2,3,4,20,21)

try:
    # 신호등 작동 반복
    while 1:
        # (0,0,1,1,0)
        # → 각 핀의 ON/OFF 상태 설정 (0=꺼짐, 1=켜짐)
        # 예: 4번, 20번 LED 켜짐
        leds.value = (0,0,1,1,0)
        sleep(3.0)  # 3초 대기

        # (0,1,0,1,0)
        # → 3번, 20번 LED 켜짐 (노란불 / 보행자 빨간불 느낌)
        leds.value = (0,1,0,1,0)
        sleep(1.0)  # 1초 대기

        # (1,0,0,0,1)
        # → 2번, 21번 LED 켜짐 (차량 빨간불 / 보행자 초록불)
        leds.value = (1,0,0,0,1)
        sleep(3.0)  # 3초 대기

# Ctrl+C 눌러서 종료할 때 예외 처리
except KeyboardInterrupt:
    pass

# 프로그램 완료 후 모든 LED 끄기
leds.off()
