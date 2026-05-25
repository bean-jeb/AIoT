import cv2
from gpiozero import Buzzer
import time

# 라즈베리 파이의 GPIO 16번 핀에 연결된 알람용 부저 객체 생성
buzzerPin = Buzzer(16)

def main():
    # 시스템에 연결된 기본 웹캠 장치를 비디오 캡처 객체로 활성화
    camera = cv2.VideoCapture(-1)
    # 프레임 해상도 너비를 640 픽셀로 설정
    camera.set(3,640)
    # 프레임 해상도 높이를 480 픽셀로 설정
    camera.set(4,480)
    
    # OpenCV에 내장된 정면 얼굴 인식용 사전 학습 xml 모델의 절대 경로 지정
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    # OpenCV에 내장된 눈 인식용 사전 학습 xml 모델의 절대 경로 지정
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'
    
    # 지정한 xml 파일을 바탕으로 객체 인식 머신러닝 분류기 인스턴스 생성
    face_cascade = cv2.CascadeClassifier(face_xml)
    eye_cascade = cv2.CascadeClassifier(eye_xml)
    
    # 카메라 장치가 정상적으로 열려 있는 동안 영상 처리를 위한 무한 반복 수행
    while( camera.isOpened() ):
        # 카메라로부터 현재 프레임 이미지를 읽어옴
        _, image = camera.read()
        # 연산 속도 향상을 위해 BGR 컬러 프레임을 그레이스케일(흑백) 이미지로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 흑백 프레임에서 얼굴 객체 탐지 수행 후 탐지된 얼굴들의 좌표와 크기 반환
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)
        # 터미널 창에 현재 탐지된 얼굴의 총 개수를 문자열로 출력
        print("faces detected Number: " + str(len(faces)))

        # 화면 내에 얼굴이 한 개 이상 탐지되었을 경우 실행되는 블록
        if len(faces):
            # 탐지된 각각의 얼굴 좌표(x,y)와 너비(w), 높이(h)를 순회
            for (x,y,w,h) in faces:
                # 원본 컬러 이미지의 얼굴 영역에 파란색 사각형 테두리 렌더링
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                
                # 눈 탐지의 정확도를 높이기 위해 화면 전체가 아닌 얼굴 영역(ROI)만 분리하여 추출
                face_gray = gray[y:y+h, x:x+w]
                face_color = image[y:y+h, x:x+w]
                
                # 추출된 얼굴 영역 내부에서 눈 객체 탐지 수행
                eyes = eye_cascade.detectMultiScale(face_gray,scaleFactor=1.1,minNeighbors=5)
                
                # 탐지된 눈의 개수가 1개 이하일 경우 (눈을 감았거나 졸음 상태로 간주)
                if len(eyes) <= 1:
                    # 하드웨어 알람 부저 작동
                    buzzerPin.on()
                # 탐지된 눈의 개수가 2개 이상일 경우 (눈을 뜬 정상 상태로 간주)
                else:
                    # 하드웨어 알람 부저 중단
                    buzzerPin.off()
                
                # 탐지된 눈의 세부 위치를 순회하며 초록색 사각형 테두리 렌더링
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
        
        # 가공된 최종 프레임 이미지를 'result'라는 이름의 윈도우 창에 출력
        cv2.imshow('result', image)
        
        # 1ms 단위로 키보드 입력을 감지하며 'q' 키가 입력되면 루프 강제 탈출
        if cv2.waitKey(1) == ord('q'):
            break
    
    # 캡처 루프 종료 후 생성된 모든 OpenCV 윈도우 창 소멸
    cv2.destroyAllWindows()
    # 프로그램 종료 전 켜져 있을지 모르는 부저 작동을 안전하게 중단
    buzzerPin.off()

# 현재 스크립트가 메인 모듈로 직접 실행될 경우 main 함수를 호출하여 시스템 가동
if __name__ == '__main__':
    main()