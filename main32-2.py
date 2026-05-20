import speech_recognition as sr
import requests
import os
import time

# 기상 정보 획득을 위한 OpenWeatherMap API 인증 키 및 대상 지역 URL 설정
API_KEY = "cced838f4b13967df350a2a155107e27"
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

# espeak 외부 소프트웨어를 호출하여 텍스트를 음성으로 변환하는 함수 정의
def speak(option, msg):
    # os.system을 통해 시스템 터미널에서 espeak 명령어 실행
    os.system("espeak {} '{}'".format(option, msg))

try:
    while True:
        # 구글 음성 인식을 위한 Recognizer 객체를 매 루프마다 초기화하여 생성
        r = sr.Recognizer()
        
        # 시스템의 기본 마이크를 오디오 입력 소스로 설정
        with sr.Microphone() as source:
            print("Say something!")
            # 마이크 입력을 대기하며 사용자의 오디오 데이터를 수신
            audio = r.listen(source)
            
        try:
            # 구글 웹 음성 인식 엔진을 활용하여 한국어 음성 데이터를 텍스트로 변환(STT)
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)
            
            # 변환된 텍스트에 '날씨'라는 핵심 키워드가 포함되어 있는지 조건 판별
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.")
                
                # requests 라이브러리를 사용하여 OpenWeatherMap API 서버에 기상 데이터 요청
                response = requests.get(url)
                # 수신된 응답 데이터를 JSON 파이썬 딕셔너리 구조로 파싱
                data = response.json()
                
                # 기상 데이터 구조에서 현재 온도와 습도 값을 추출
                temp = data["main"]["temp"]
                humi = data["main"]["humidity"]
                
                # 안내할 기상 정보를 음성 출력용 문자열 포맷으로 조립 (온도는 정수형으로 변환)
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                # espeak 옵션 설정 (-s: 속도 180, -p: 음고 50, -a: 볼륨 200, -v: 한국어 여성 음색 5번)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                # 정제된 옵션과 조립된 메시지를 바탕으로 음성 합성 함수 실행(TTS)
                speak(option, msg)
            
        except sr.UnknownValueError:
            # 음성 파형이 불명확하거나 주변 소음으로 인해 발화 내용을 인지하지 못했을 때의 예외 처리
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # 네트워크 단절 등으로 구글 웹 서비스 통신에 실패했을 때의 예외 처리
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    # 사용자가 강제 종료(Ctrl+C)를 입력할 경우 안전하게 무한 루프를 탈출
    pass