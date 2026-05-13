import paho.mqtt.client as mqtt  # MQTT 프로토콜 통신을 가능하게 하는 외부 라이브러리 로드
import time                      # 시간 지연(sleep) 기능을 사용하기 위한 모듈
from gpiozero import LED         # 라즈베리 파이의 GPIO 핀을 제어하여 LED를 끄고 켜는 라이브러리
import threading                 # 두 가지 작업(메시지 수신/데이터 전송)을 동시에 하기 위한 병렬 처리 모듈

# 라즈베리 파이의 실제 확장 핀(GPIO) 16, 20, 21번에 LED 객체 할당
greenLed = LED(16)
blueLed = LED(20)
redLed = LED(21)

# [콜백 함수] 브로커로부터 내가 구독한 토픽의 메시지가 도착했을 때 실행되는 함수
def on_message(client, userdata, msg):
    # msg.topic: 어떤 주제로 왔는지, msg.payload: 실제 데이터 내용 (바이트 형태)
    print(msg.topic + " " + str(msg.payload)) 
    
    # 네트워크를 통해 들어온 데이터(바이트)를 파이썬에서 읽을 수 있는 문자열로 변환(decode)
    message = msg.payload.decode()
    print("수신된 메시지:", message)
    
    # 수신된 문자열 값에 따라 각 색상의 LED 상태를 물리적으로 제어
    if message == "green_on":
        greenLed.on()   # 16번 핀에 전원 공급
    elif message == "green_off":
        greenLed.off()  # 16번 핀 전원 차단
    elif message == "blue_on":
        blueLed.on()
    elif message == "blue_off":
        blueLed.off()
    elif message == "red_on":
        redLed.on()
    elif message == "red_off":
        redLed.off()

# MQTT 클라이언트 인스턴스 생성
client = mqtt.Client()
# 메시지가 왔을 때 위에서 정의한 on_message 함수가 작동하도록 연결
client.on_message = on_message

# 라즈베리 파이(브로커)의 고유 IP 주소 설정
broker_address = "192.168.137.230" 
# 설정한 IP 주소로 MQTT 서버에 접속 시도
client.connect(broker_address)
# "led"라는 주제(Topic)로 들어오는 신호를 감시하겠다고 선언 (QoS 레벨 1 설정)
client.subscribe("led", 1)

count = 0
# 별도의 통로(스레드)에서 무한히 반복 실행될 함수 정의
def send_thread():
    global count
    while 1:
        count = count + 1
        # "hello"라는 주제로 현재 count 숫자를 문자열로 바꾸어 전송(Publish)
        client.publish("hello", str(count))
        # 1초 동안 대기 후 루프 반복
        time.sleep(1.0)

# send_thread 함수를 별도의 작업 스레드로 지정하여 백그라운드에서 실행 준비
task = threading.Thread(target=send_thread)
task.start() # 백그라운드 작업 시작 (숫자 전송 시작)

# 메인 스레드는 여기서 무한 대기하며 외부에서 오는 "led" 관련 메시지를 계속 수신함
client.loop_forever()
