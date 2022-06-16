from cgi import test
from email.mime import image
import math
import threading
import RPi.GPIO as GPIO
import time
from tkinter import *
from PIL import Image, ImageTk

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 서보모터의 핀 번호 및 설정
SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)
# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)

# LED핀의 번호 및 설정
led_pin = 14
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, 0)

speed = 0.1

trig = 23
echo = 24

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.output(trig, False)
time.sleep(1)

callitem = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']]

# 설정된 비밀번호가 존재하는지에 대한 변수.
PW_EXIST = False
# 문이 열려있는지 닫혀있는지에 대한 변수
Isopen = False

password = []

disvalue = ""

def open():
    global PW_EXIST, password, Isopen
    e = input_pw.get()
    if len(e) == 0:
        plz_input_label = Label(frame, text="비밀번호를 입력해주세요!", fg='red')
        plz_input_label.place(x=100, y=200)
        plz_input_label.after(2000, lambda : plz_input_label.destroy())
        return
    elif len(e)>=1 and e[0] == '*':
        PW_EXIST = True
        for i in range(len(e)-1):
            password.append(e[i+1])

    if not PW_EXIST:
        pw_not_exist_label = Label(frame, text="비밀번호가 존재하지 않습니다.", fg='red')
        pw_not_exist_label.place(x=100, y=200)
        clear()
        pw_not_exist_label.after(3000, lambda: pw_not_exist_label.destroy())
    elif PW_EXIST:
        if password != list(e):
            pw_not_match_label = Label(frame, text="비밀번호가 일치하지 않습니다.", fg='red')
            pw_not_match_label.place(x=100, y=200)
            clear()
            pw_not_match_label.after(2000, lambda: pw_not_match_label.destroy())
            X_label = Label(frame, image=image_X_tk)
            X_label.place(x=150, y=280)
            X_label.after(2000, lambda: X_label.destroy())
        else:
            clear()
            GPIO.output(led_pin, 1)
            if not Isopen:
                Isopen = True
                close_locker_label.place_forget()
                open_locker_label.place(x=25, y=50)
            open_msg_label = Label(frame, text="문이 열렸습니다", fg='blue')
            open_msg_label.place(x=100, y=200)
            O_label = Label(frame, image=image_O_tk)
            O_label.place(x=150, y=280)
            open_msg_label.after(2000, lambda: open_msg_label.destroy())
            O_label.after(2000, lambda: O_label.destroy())
            motor(True)

def close():
    global Isopen
    GPIO.output(led_pin, 0)
    if Isopen:
        Isopen = False
        open_locker_label.place_forget()
        close_locker_label.place(x=25, y=50)
    close_msg_label = Label(frame, text="문이 닫혔습니다.")
    close_msg_label.place(x=100, y=200)
    close_msg_label.after(2000, lambda: close_msg_label.destroy())
    motor(False)
    

def pw_click(item):
    ast_click(item)

def ast_click(item):
    global disvalue
    disvalue = disvalue + item
    str_value.set(disvalue)

def clear():
    global disvalue
    disvalue = ""
    str_value.set(disvalue)

def motor(bool):
    if bool:
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        servo.start(0)
        servo.ChangeDutyCycle(7.5)  # 90도
        time.sleep(0.5)
        GPIO.setup(SERVO_PIN, GPIO.IN)
    else:
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        servo.start(0)
        servo.ChangeDutyCycle(2.5)  # 0도
        time.sleep(0.5)
        GPIO.setup(SERVO_PIN, GPIO.IN)

def dist():
    while True:
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
        
        if(distance <= 10):
            #locker_status_now.config(text="물건 존재")
            box_label.place(x=90, y=95)
        if(distance > 10):
            #locker_status_now.config(text="물건 미존재")
            box_label.place_forget()

frame = Tk() # 프레임 생성
frame.geometry("270x420") # 프레임 크기 설정

str_value = StringVar()
str_value.set("")

# O 이미지를 불러오고 크기 조정
image_O = Image.open("/home/pi/Desktop/O.png")
image_O_resize = image_O.resize((100, 100))
image_O_tk = ImageTk.PhotoImage(image_O_resize)

# X 이미지를 불러오고 크기 조정
image_X = Image.open("/home/pi/Desktop/X.png")
image_X_resize = image_X.resize((100, 100))
image_X_tk = ImageTk.PhotoImage(image_X_resize)

# 닫힌 로커 이미지를 불러오고 크기 조정
image_close = Image.open("/home/pi/Desktop/close_locker2.png")
image_close_resize = image_close.resize((200, 120))
image_close_tk = ImageTk.PhotoImage(image_close_resize)

# 열린 로커 이미지를 불러오고 크기 조정
image_open = Image.open("/home/pi/Desktop/open_locker.png")
image_open_resize = image_open.resize((200, 120))
image_open_tk = ImageTk.PhotoImage(image_open_resize)

# 박스 이미지 불러오고 크기 조정
image_box = Image.open("/home/pi/Desktop/box5.png")
image_box_resize = image_box.resize((100, 57))
image_box_tk = ImageTk.PhotoImage(image_box_resize)

# 열린 로커 이미지 배치 후 숨김
open_locker_label = Label(frame, image=image_open_tk)
open_locker_label.place(x=25, y=50)
open_locker_label.place_forget()

# 박스 이미지 배치 후 숨김
box_label = Label(frame, image=image_box_tk)
box_label.place(x=90, y=95)
box_label.place_forget()

# 닫힌 로커 이미지 배치 좌표
close_locker_label = Label(frame, image=image_close_tk)
close_locker_label.place(x=25, y=50)

locker_status= Label(frame, text="사물함 상황 : ", font=900)
locker_status.place(x=20, y=10)
locker_status_now = Label(frame, text="물건 미존재", font=900)
locker_status_now.place(x=130, y=10)

pw_label = Label(frame, text="비밀번호", font=100)
pw_label.place(x=20, y=200)

input_pw = Entry(frame, text=str_value, width=14)
input_pw.place(x=20, y=230)

open_btn = Button(frame, text="열기", command=lambda : open())
open_btn.place(x=150, y=225)

close_btn = Button(frame, text="닫기", command=lambda : close())
close_btn.place(x=210, y=225)

for i,items in enumerate(callitem):
    for j,item in enumerate(items):
        #btn = Button(frame, text=item, command=pw_click(item))
        btn = Button(frame, text=item, command=lambda cmd=item: pw_click(cmd))
        btn.place(x=20+40*j, y=260+40*i)


t1 = threading.Thread(target=dist, args=())
t1.start()

frame.mainloop()



