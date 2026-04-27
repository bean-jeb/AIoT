from flask import Flask, request, render_template
from gpiozero import LED

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# Raspberry Pi의 GPIO 21번 핀에 연결된 LED 설정
red_led = LED(21)   

# 기본 경로('/') 접속 시 실행되는 함수
@app.route('/')
def home():
    # templates 폴더 내의 index.html 파일을 렌더링하여 사용자에게 전송
    return render_template("index.html")

# '/data' 경로로 POST 방식의 데이터가 들어올 때 실행되는 함수
@app.route('/data', methods = ['POST'])
def data():
    # HTML 폼(form)에서 전달된 led 이름의 데이터를 가져옴
    data = request.form['led']
    
    # 전달받은 값이 'on'일 경우 LED 점등
    if(data == 'on'):
        red_led.on() 
        # 제어 후 다시 홈 화면으로 복귀
        return home()

    # 전달받은 값이 'off'일 경우 LED 소등
    elif(data == 'off'):
        red_led.off() 
        # 제어 후 다시 홈 화면으로 복귀
        return home() 

# 스크립트가 직접 실행될 때 웹 서버 가동
if __name__ == '__main__':
    # 모든 네트워크 인터페이스(0.0.0.0)에서 80번 포트로 접속 허용
    app.run(host = '0.0.0.0', port = '80')