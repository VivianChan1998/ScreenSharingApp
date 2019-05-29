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
                        
                cv2.imshow('hi',frame)                                          #顯示畫面

                i+=1
                        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                            
            except:
                             
                data = s.recv(6000000)                              #傳送中出現錯誤,清空buffer
                print(":(")
                        
        except:
            pass
                    
        s.sendall(str.encode('ack'))     


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
            #time.sleep(0.0001)         
            data  = s.recv(1000000000) #再加0 compile會過不了
            data2 = s.recv(1000000000)
            data3 = s.recv(1000000000)
            data = data + data2 + data3
                
            try:                                                                    #將接收的RGB陣列寫到jpg檔中再打開
                    
                with open('save.jpeg','wb') as f:
                    f.write(data)

                try:
                        
                    global frame
                    frame = cv2.imread('save.jpeg')
                    cv2.imshow('Server', frame)
                    if cv2.waitKey(100) == ord('q'):
                        cv2.destroyAllWindows()
                        break
                            
                except:
                    data = s.recv(100000000)
                    print(":(")
                    
            except:
                print('except')
                pass
                    
            #s.sendall(str.encode('ack'))
        

    recscreen()


if __name__ == "__main__" :
    HOST, PORT = "118.233.68.7", 61676
    # HOST, PORT = "140.112.226.236", 61677
    # HOST, PORT = "163.13.137.71", 61677
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('connected to %s' % HOST)

    # 1 camera
    # recvideo()

    # 2 screen
    # press "q" to close the screen
    video()

    # 3 text (on terminal)
    # Thread(target = send).start()
    # Thread(target = receive).start()

