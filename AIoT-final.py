import asyncio
import urllib.request
import json
import datetime
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from gpiozero import MotionSensor, LED
import time

# 텔레그램 봇 토큰 및 수신자 아이디 설정
telegram_id = '8713438311'
my_token = '8706778080:AAFdCvlTybtqG-LxW_DQBBiU_oH7Cx-8qfc'
# 기상 데이터 수집을 위한 OpenWeatherMap API 인증 키
api_key = 'cced838f4b13967df350a2a155107e27'

# 하드웨어 제어를 위한 GPIO 핀 번호 할당
PIR_PIN = 16
LED_ALERT_PIN = 17    # 정보 수집 및 전송 상태를 시각화하는 적색 및 청색 LED 핀
LED_STANDBY_PIN = 27  # 감지 대기 상태를 나타내는 녹색 LED 핀

# gpiozero 라이브러리를 활용한 물리적 하드웨어 객체 초기화
pir = MotionSensor(PIR_PIN)
led_alert = LED(LED_ALERT_PIN)
led_standby = LED(LED_STANDBY_PIN)

# OpenWeatherMap API를 호출하여 향후 12시간 동안의 기상 정보를 수집하는 동기 함수
def getWeather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=kr&cnt=4"
    try:
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
        
        text = ""
        # 3시간 간격으로 제공되는 4개의 예보 데이터를 순회하며 문자열로 조립
        for i in range(4):
            item = data['list'][i]
            # 협정 세계시를 한국 표준시로 변환하여 24시간제 문자열로 가공
            hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            text += f" - {hour}시 {temp}°C, {desc}\n"
        return text
    except Exception as e:
        return f"날씨 정보 로드 실패 {e}"

# 네이버 금융 웹페이지를 크롤링하여 특정 종목의 현재 주가를 수집하는 동기 함수
def get_price(com_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + com_code
    try:
        # 정상적인 브라우저 접근으로 인식되도록 User-agent 헤더 추가
        result = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        bs_obj = BeautifulSoup(result.content, "html.parser")
        # HTML 구조 내에서 현재가 정보를 담고 있는 특정 태그와 클래스를 역추적하여 데이터 추출
        no_today = bs_obj.find("p", {"class":"no_today"})
        blind_now = no_today.find("span", {"class":"blind"})
        return blind_now.text
    except Exception as e:
        return f"주가 정보 로드 실패 {e}"

# 하드웨어 감시와 데이터 수집 및 알림 전송을 총괄하는 메인 비동기 루프
async def main():
    bot = Bot(token=my_token)
    last_alert_time = 0
    # 과도한 중복 알림을 방지하기 위한 60초 단위의 재가동 대기 시간 설정
    COOLDOWN_SEC = 60  

    print("시스템 부팅 완료 감지 대기 중...")
    
    try:
        while True:
            # 쿨다운 시간이 경과하였고 대기등이 꺼져있을 경우 녹색 대기등 점등 및 알림등 소등
            if not led_standby.is_active and (time.time() - last_alert_time > COOLDOWN_SEC):
                led_standby.on()
                led_alert.off()

            # PIR 센서로부터 인체 움직임이 감지되었을 때 실행되는 조건문
            if pir.value == 1:
                current_time = time.time()
                
                # 마지막 알림으로부터 60초가 경과한 시점에만 새로운 브리핑 프로세스 가동
                if current_time - last_alert_time > COOLDOWN_SEC:
                    # 사용자에게 시스템이 작동 중임을 알리기 위해 녹색등을 끄고 처리등을 켬
                    led_standby.off()
                    led_alert.on() 
                    
                    # 현재 시각을 문자열로 기록하고 터미널에 감지 로그 출력
                    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H시 %M분 %S초')
                    print(f"[{now_str}] 외출 감지 정보 수집 및 브리핑 전송 시작...")
                    
                    # 네트워크 지연으로 인한 하드웨어 제어 블로킹을 방지하기 위해 동기 함수들을 별도 스레드로 분리
                    weather_task = asyncio.to_thread(getWeather)
                    price_task = asyncio.to_thread(get_price, "005930")
                    
                    # 분리된 두 개의 데이터 수집 스레드가 모두 완료될 때까지 비동기적으로 대기
                    weather_msg, price_msg = await asyncio.gather(weather_task, price_task)
                    
                    # 수집된 날씨와 주식 정보를 사용자가 읽기 편한 하나의 통합 문자열로 포맷팅
                    final_msg = (
                        f"🏃 외출 및 접근 감지 브리핑\n"
                        f"🕒 {now_str}\n\n"
                        f"🌤 [오늘의 날씨]\n{weather_msg}\n"
                        f"📈 [삼성전자 주가]\n현재가 {price_msg}원"
                    )
                    
                    # 완성된 브리핑 메시지를 텔레그램 서버를 통해 사용자의 스마트폰으로 비동기 전송
                    await bot.send_message(chat_id=telegram_id, text=final_msg)
                    print("텔레그램 브리핑 전송 완료.")
                    
                    # 시스템 타이머를 현재 시각으로 갱신하고 처리등을 소등하여 초기화 준비
                    last_alert_time = current_time
                    led_alert.off()
                    
            # 센서 감지 루프의 CPU 점유율을 최적화하고 다른 비동기 작업에 제어권을 넘기기 위한 짧은 휴지
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        # 사용자의 강제 종료 인터럽트 발생 시 하드웨어 핀 상태를 안전하게 초기화
        print("\n프로그램을 안전하게 종료합니다.")
        led_standby.off()
        led_alert.off()

# 스크립트 직접 실행 시 메인 비동기 함수 가동
if __name__ == '__main__':
    asyncio.run(main())