
# gpiozero 라이브러리에서 MotionSensor 클래스 불러오기
from gpiozero import MotionSensor
# time 라이브러리 불러오기
import time
# picamera2 라이브러리에서 Picamera2 클래스 불러오기
from picamera2 import Picamera2
# 날짜/시간 처리를 위한 datetime 라이브러리 불러오기
import datetime

# PIR 모션 센서 입력 핀으로 GPIO 16번 핀 초기화
pirPin = MotionSensor(16)

# Picamera2 객체 생성
picam2 = Picamera2()
# 카메라 미리보기 설정
camera_config = picam2.create_preview_configuration()
# 카메라에 설정 적용
picam2.configure(camera_config)
# 카메라 시작
picam2.start()

# 무한 루프 시작
try:
    while True:
        try:
            # PIR 센서의 현재 값을 읽어 변수에 저장
            sensorValue = pirPin.value
            # 센서 값이 1 -> 움직임이 감지된 것으로 판단
            if sensorValue == 1:
                # 터미널에 감지된 시각 출력
                now = datetime.datetime.now()
                print(now)
                # 시각을 파일명 형식 문자열로 변환
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')
                # 해당 파일명으로 jpg 사진 촬영 및 저장
                picam2.capture_file(fileName + '.jpg')
                # 0.5초 대기 -> 연속 촬영 방지
                time.sleep(0.5)
        # 촬영 중 오류 발생 시 -> 무시하고 계속 진행
        except:
            pass

# 키보드 인터럽트(Ctrl+C) -> 루프 종료
except KeyboardInterrupt:
    pass

