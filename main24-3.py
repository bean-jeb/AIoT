import urllib.request, json, tkinter, tkinter.font

# OpenWeatherMap에서 발급받은 개인 API 키 설정
API_KEY = "cced838f4b13967df350a2a155107e27"

# 1분(60초)마다 날씨 정보를 업데이트하는 함수 정의
def tick1Min():
    # 서울 지역의 온습도 데이터를 요청하는 URL 생성 (단위: 섭씨/metric)
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
    
    # urllib를 사용하여 API 서버에 접속 및 데이터 수신
    with urllib.request.urlopen(url) as r:
        # 수신된 JSON 형식의 데이터를 파이썬 딕셔너리로 변환
        data = json.loads(r.read())
        
    # JSON 구조에서 온도(temp)와 습도(humidity) 데이터 추출
    temp = data["main"]["temp"]
    humi = data["main"]["humidity"]
    
    # GUI 레이블의 텍스트를 최신 정보로 업데이트 (소수점 1자리까지 표시)
    label.config(text=f"{temp:.1f}C   {humi}%")
    
    # 60,000ms(1분) 후에 다시 tick1Min 함수를 호출하도록 예약 (재귀적 반복)
    window.after(60000, tick1Min)

# Tkinter 메인 윈도우 창 설정
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY") # 창 제목 설정
window.geometry("400x100")        # 창 크기 설정 (가로 400, 세로 100)
window.resizable(False, False)    # 창 크기 조절 불가 설정

# 출력용 폰트 설정 (크기 30)
font = tkinter.font.Font(size=30)

# 온습도 정보를 표시할 레이블 위젯 생성 및 배치
label = tkinter.Label(window, text="", font=font)
label.pack()

# 최초 1회 함수 실행을 통해 데이터 수신 시작
tick1Min()

# GUI 이벤트 루프 시작 (창 유지)
window.mainloop()