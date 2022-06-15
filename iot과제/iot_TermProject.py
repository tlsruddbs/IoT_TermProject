from email.mime import image
from multiprocessing import Process
import threading
import pymysql
import RPi.GPIO as GPIO
import time
from tkinter import *
from PIL import Image, ImageTk

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

speed = 0.5

trig1 = 23
echo1 = 24

trig2 = 2
echo2 = 3

trig3 = 17
echo3 = 27

trig4 = 10
echo4 = 9

GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.output(trig1, False)
time.sleep(1)

GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(echo2,GPIO.IN)
GPIO.output(trig2, False)
time.sleep(1)

GPIO.setup(trig3,GPIO.OUT)
GPIO.setup(echo3,GPIO.IN)
GPIO.output(trig3, False)
time.sleep(1)

GPIO.setup(trig4,GPIO.OUT)
GPIO.setup(echo4,GPIO.IN)
GPIO.output(trig4, False)
time.sleep(1)

print("gpio setup complete")

# 각 주차자리 번호에 차를 위치시킬 x, y 좌표
spot1 = (80, 70)
spot2 = (180, 70)
spot3 = (80, 220)
spot4 = (180, 220)

frame = Tk() # 프레임 생성
frame.geometry("350x550") # 프레임 크기 설정

# 주차장 이미지를 불러오고 크기 조정
image_park = Image.open("/home/pi/Desktop/parkingspot.png")
image_park_resize = image_park.resize((300, 263))

# 차 이미지를 불러오고 크기 조정
image_car = Image.open("/home/pi/Desktop/car.png")
image_car_resize = image_car.resize((60, 70))

# 프레임에 주차장 이미지 배치
image_park_tk = ImageTk.PhotoImage(image_park_resize)
parklabel = Label(frame, image=image_park_tk)
parklabel.place(x=10, y=50)

# 프레임에 차 이미지 배치
image_car_tk = ImageTk.PhotoImage(image_car_resize)
# carlabel = Label(frame, image=image_car_tk)
# carlabel.place(x=80, y=220)

park_status= Label(frame, text="주차 현황: ", font=100)
park_status.place(x=20, y=10)
park_status_num = Label(frame, text="2 / 4", font=100) # 나중에 2 분리할것.
park_status_num.place(x=100, y=10)

price_status = Label(frame, text="요금 현황: ", font=100)
price_status.place(x=20, y=330)

park_spot1 = Label(frame, text="1번 자리: ", font=100)
park_spot1.place(x=50, y=360)
park_spot2 = Label(frame, text="2번 자리: ", font=100)
park_spot2.place(x=50, y=390)
park_spot3 = Label(frame, text="3번 자리: ", font=100)
park_spot3.place(x=50, y=420)
park_spot4 = Label(frame, text="4번 자리: ", font=100)
park_spot4.place(x=50, y=450)

price_spot1 = Label(frame, text="10000", font=100)
price_spot1.place(x=130, y=360)
price_spot2 = Label(frame, text="7000", font=100)
price_spot2.place(x=130, y=390)
price_spot3 = Label(frame, text="13000", font=100)
price_spot3.place(x=130, y=420)
price_spot4 = Label(frame, text="4000", font=100)
price_spot4.place(x=130, y=450)



def distance(trig, echo):
    # global start, stop
    GPIO.output(trig, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
    time.sleep(0.00001)       # 10µs 딜레이 
    GPIO.output(trig, False)

    while GPIO.input(echo)==0:
        start = time.time()	 # Echo 핀 상승 시간 
    while GPIO.input(echo)==1:
        stop= time.time() # Echo 핀 하강 시간 

    check_time = stop - start
    distance = check_time * 34300 / 2
    print("Distance : %.1f cm" % distance)
    time.sleep(0.4)	# 0.4초 간격으로 센서 측정 

    return distance

    # if(distance <= 10):
    #     price_spot1.config(text="0")
    #     image_car_tk_1 = ImageTk.PhotoImage(image_car_resize)
    #     spot1_carlabel = Label(frame, image=image_car_tk_1)
    #     spot1_carlabel.place(x=spot1[0], y=spot1[1])
    #     time.sleep(speed)
    # elif(distance > 10):
    #     time.sleep(speed)

def measure_dist():
    while True:
        first_dist = distance(trig1, echo1)
        # second_dist = distance(trig2, echo2)
        # third_dist = distance(trig3, echo3)
        # fourth_dist = distance(trig4, echo4)

        if(first_dist <= 10):
            price_spot1.config(text="0")
            # image_car_tk_1 = ImageTk.PhotoImage(image_car_resize)
            spot1_carlabel = Label(frame, image=image_car_tk)
            spot1_carlabel.place(x=spot1[0], y=spot1[1])
        # if(second_dist <= 10):
        #     price_spot2.config(text="0")
        #     # image_car_tk_1 = ImageTk.PhotoImage(image_car_resize)
        #     spot2_carlabel = Label(frame, image=image_car_tk)
        #     spot2_carlabel.place(x=spot2[0], y=spot2[1])
        # if(third_dist <= 10):
        #     price_spot3.config(text="0")
        #     # image_car_tk_1 = ImageTk.PhotoImage(image_car_resize)
        #     spot3_carlabel = Label(frame, image=image_car_tk)
        #     spot3_carlabel.place(x=spot3[0], y=spot3[1])
        # if(fourth_dist <= 10):
        #     price_spot4.config(text="0")
        #     # image_car_tk_1 = ImageTk.PhotoImage(image_car_resize)
        #     spot4_carlabel = Label(frame, image=image_car_tk)
        #     spot4_carlabel.place(x=spot4[0], y=spot4[1])

t1 = threading.Thread(target=measure_dist, args=())
t1.start()

# p_a = Process(target=doit)
# p_a.start()

frame.mainloop()



