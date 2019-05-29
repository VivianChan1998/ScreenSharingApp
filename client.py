# import speech_recognition
import cv2
from threading import Thread
from threading import Lock
import socket
# import tkinter
import time
import pickle
from PIL import Image
from functools import partial
import numpy as np
# from tkinter import *
# import tkinter.messagebox
from random import randint


DANMU=list()

# for sending text on terminal
def send():
    while True:
        content = input()
        s.send(content.encode('utf-8'))


# for receiving text on terminal
def receive():
    while True:
        response = s.recv(1024)
        print(response.decode('utf-8'))

'''
# This is for camera
def recvideo():

    global lock
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    i=0
    minute=0
    sec=0
    clock = time.time()                                                         #計時
    sliding = 0                                                                 #彈幕滑動

    while 1:                                                                    #讀取對方的視訊
                     
        data = s.recv(3000000)
                
        try:                                                                    #將接收的RGB陣列寫到jpg檔中再打開
                    
            with open('save.jpg','wb') as f:
                f.write(data)

            try:
                        
                global frame
                frame = cv2.imread('save.jpg')

                #frame = cv2.medianBlur(frame, 5)  
                #frame = cv2.filter2D(frame, -1, kernel)
                
                counter = int (time.time()-clock)
                minute = int (counter/60)
                sec = int (counter%60)

                for e in DANMU:
        
                    e[1] += 10
                    cv2.putText(frame, e[0], (550-e[1],e[2]), cv2.FONT_HERSHEY_SIMPLEX,2,(34,195,46),1, cv2.LINE_AA)

                    if e[1] == 550:
                        DANMU.pop(0)

                cv2.putText(frame, str(minute) + ':' + str(sec), (0,86), cv2.FONT_HERSHEY_SIMPLEX,2,(34,195,46),1, cv2.LINE_AA)
                cv2.putText(frame, str(i), (0,40), cv2.FONT_HERSHEY_SIMPLEX,2,(34,195,46),1, cv2.LINE_AA)
                
                cv2.imshow('Server', frame)                                          #顯示畫面

                i+=1
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                            
            except:
                             
                data = s.recv(6000000)                              #傳送中出現錯誤,清空buffer
                print(":(")
                        
        except:
            pass
                    
        s.sendall(str.encode('ack'))     
'''

a = ''
def sndvideo():                                                                         #傳

    global a
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,450)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,450)

    resolution = 0                                                                      #解析度變數
    dev = 0
    estimate = 0.1                                                                      #設定的標準傳送秒數
    add = 0                                                                             #隨網路速度做視訊大小增減的變數(連續3包)
    sub = 0
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        
        cv2.putText(frame, a, (100,250), cv2.FONT_HERSHEY_SIMPLEX,1,(0,71,171),2, cv2.LINE_AA)             
        cv2.imwrite('buffer.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, 25])

        if count > 30:
            count = 0
            a=''

        else:
            count+=1
        
        try:
                    
            start = time.time()
            with open('buffer.jpg','rb') as f:
                s.sendall(f.read())
            
            ack = s.recv(128)
            sample = time.time()- start

            #estimate = (1-0.125)*estimate + 0.125*sample
            #dev = (1-0.25)*dev + 0.25*abs(sample - estimate)
            timeout = estimate +4*dev

            # if sample < timeout - 0.07:                                                 #隨著偵測網路速度做視訊大小調整
            #     add +=1
            #     if(add >=5):
            #         resolution += 10
            #         cap.set(cv2.CAP_PROP_FRAME_WIDTH,400+resolution)
            #         cap.set(cv2.CAP_PROP_FRAME_HEIGHT,400+resolution)

            # elif sample > timeout + 0.07:                                               #隨著網路速度做視訊大小調整
            #     sub += 1
            #     if(sub >=5):
            #         resolution -= 10
            #         cap.set(cv2.CAP_PROP_FRAME_WIDTH,400+resolution)
            #         cap.set(cv2.CAP_PROP_FRAME_HEIGHT,400+resolution)

            # else:
            #     add =0
            #     sub =0
                                       
                    
        except:
            pass

# This is for screen
def video():
    def recscreen():  
        
        global lock
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        i=0
        minute=0
        sec=0
        clock = time.time()                                                         #計時
        sliding = 0                                                                 #彈幕滑動
        
        while 1:                                                                    #讀取對方的視訊
                     
            data = s.recv(1000000000)
            data2 = s.recv(1000000000)
            data3 = s.recv(1000000000)
            data4 = s.recv(1000000000)
            data5 = s.recv(1000000000)
            data = data + data2 + data3 + data4 + data5
                
            try:                                                                    #將接收的RGB陣列寫到jpg檔中再打開
                    
                with open('save.jpg','wb') as f:
                    f.write(data)

                try:
                        
                    global frame
                    frame = cv2.imread('save.jpg') 
                    
                    cv2.imshow('Server', frame)
                    
                    if cv2.waitKey(100) == ord('q'):
                        cv2.destroyAllWindows()
                        break
                            
                except:
                    pass
                    #data = s.recv(1000000)
                    #print(":(")
                    
            except:
                print('except')
                pass
                    
            # s.sendall(str.encode('ack'))
        

    recscreen()


if __name__ == "__main__" :
    # HOST, PORT = "127.0.0.1", 61677
    # HOST, PORT = "140.112.226.236", 61677
    HOST, PORT = "163.13.137.71", 61677
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('connected to %s' % HOST)

    # 1 camera
    # press "q" to close the screen
    # recvideo()
    # sndvideo()

    # 2 screen
    # press "q" to close the screen
    video()

    # 3 text (on terminal)
    # Thread(target = send).start()
    # Thread(target = receive).start()

