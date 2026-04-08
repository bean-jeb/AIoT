
# gpiozero 라이브러리에서 DigitalInputDevice 클래스를 가져온다
from gpiozero import Buzzer, DigitalInputDevice
# time 라이브러리를 가져옴
import time

# 부저 제어 핀으로 GPIO 18번 핀 초기화
bz = Buzzer(18)
# MQ2 센서 입력 핀으로 GPIO 17번 핀 초기화
gas = DigitalInputDevice(17)

# 무한 루프 시작 -> Lines 8 ~ 18 반복함
try:
    while True:
        # DO 핀이 LOW(0) -> 가스가 감지된 것으로 판단
        if gas.value == 0:    # ← 0 = 가스 감지 (LOW)
            # 터미널에 ＂가스 감지됨＂ 출력
            print("가스 감지됨")
            # 부저 ON
            bz.on()
        # DO 핀이 HIGH(1) -> 정상 상태로 판단
        else:                 # ← 1 = 정상 (HIGH)
            # 터미널에 ＂정상＂ 출력
            print("정상")
            # 부저 OFF
            bz.off()
        # 0.2초마다 센서 값 반복 확인
        time.sleep(0.2)

# 키보드 인터럽트(Ctrl+C) -> 루프 종료
except KeyboardInterrupt:
    pass
# 프로그램 종료 시 부저를 반드시 OFF 처리
bz.off()


