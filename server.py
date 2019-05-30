import socket
import cv2
import time
from threading import Thread
# import pickle

import numpy as np
# from PIL import ImageGrab     # This does not support linux
import pyscreenshot as ImageGrab

from multiprocessing import Process
import pygame
from pygame.locals import *
import os

'''
# for sending text on terminal
def send():
    while True:
        content = input()
        client.send(content.encode('utf-8'))

# for receiving text on terminal
def receive():
    while True:
        response = client.recv(1024)
        print(response.decode('utf-8'))


def recvideo():

    global lock
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    i=0
    minute=0
    sec=0
    clock = time.time()                                                         #計時
    sliding = 0                                                                 #彈幕滑動

    while 1:                                                                    #讀取對方的視訊
                     
        data = client.recv(3000000)
                
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
                             
                data = client.recv(6000000)                              #傳送中出現錯誤,清空buffer
                print(":(")
                        
        except:
            pass
                    
        client.sendall(str.encode('ack'))
'''

# This is for screen
def video():
    def sndscreen():
        resolution = 20
        #estimate = 0.1
        #dev = 0
        #add = 0
        #sub = 0
        #count = 0

        while(True):
            screen = ImageGrab.grab(bbox=(480, 300, 1440, 900))
            screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)

            try:
                f = open('message.txt')
                message = f.read()
                f.close()
            except:
                message = ""
            
            cv2.putText(screen, message, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,153,51), 2, cv2.LINE_AA)
            cv2.imwrite('screen.jpg', screen, [cv2.IMWRITE_JPEG_QUALITY, resolution])
                    
            try:
                start = time.time()
                with open('screen.jpg','rb') as f:
                    client.sendall(f.read())
            
                #ack = client.recv(128)
                sample = time.time()- start

                if sample > 6e-5:
                    resolution = 10
                else:
                    resolution = 20

            except:
                pass
        
    sndscreen()


def type():
    temp = ''

    pygame.init()
    screen = pygame.display.set_mode((480, 360))
    font = pygame.font.Font(None, 50)

    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    temp += ' '
                elif evt.key == K_BACKSPACE:
                    temp = temp[:-1]
                elif evt.key == K_RETURN:
                    f = open('message.txt', 'w+')
                    f.write(temp)
                    f.close()
                    temp = ''
                else:
                    temp += evt.unicode
            elif evt.type == QUIT:
                return
        screen.fill((0, 0, 0))
        block = font.render(temp, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()


if __name__ == '__main__':
    HOST, PORT = "127.0.0.1", 61677
    # HOST, PORT = "140.112.226.236", 61677
    # HOST, PORT = "163.13.137.71", 61677
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print('waiting...')
    s.listen(1)

    client, address = s.accept()
    print('%s connected' % str(address))

    # 1 camera
    # press "q" to close the screen
    # sndvideo()
    # recvideo()

    # 2 screen
    # press "q" to close the screen
    # video()

    if os.path.exists('message.txt'):
        os.remove('message.txt')
    
    Process(target = type).start()
    Process(target = video).start()
    
    # 3 text (on terminal)
    # Thread(target = send).start()
    # Thread(target = receive).start()

