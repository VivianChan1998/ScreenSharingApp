import socket
import cv2
import time
import speech_recognition
import numpy as np
from PIL import Image, ImageGrab, ImageFont, ImageDraw
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
    font = ImageFont.truetype('SimSun-Bold.ttf', 28)

    def sndscreen():
        resolution = 10
        #estimate = 0.1
        #dev = 0
        #add = 0
        #sub = 0
        #count = 0

        while(True):
            try:
                f = open('message.txt')
                message = f.read()
                f.close()
            except:
                message = ""

            try:
                f = open('speech.txt')
                speech = f.read()
                f.close()
            except:
                speech = ""

            # screen = ImageGrab.grab(bbox=(480, 300, 1440, 900))
            screen = ImageGrab.grab(bbox=(640, 400, 1920, 1200)).resize((640, 400))
            
            draw = ImageDraw.Draw(screen)
            draw.text((10, 350), speech, font = font, fill = (51, 153, 255, 1))

            screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)
            
            cv2.putText(screen, message, (10, 40), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,153,51), 2, cv2.LINE_AA)
            # cv2.putText(screen, speech, (10, 350), font, 0.75, (255,153,51), 2, cv2.LINE_AA) #51, 153, 255
            cv2.imwrite('screen.jpg', screen, [cv2.IMWRITE_JPEG_QUALITY, resolution])
            
            try:
                start = time.time()
                with open('screen.jpg','rb') as f:
                    client.sendall(f.read())
            
                #ack = client.recv(128)
                # sample = time.time()- start

                # if sample > 1e-3:
                #     resolution = 10
                # else:
                #     resolution = 20
                
            except:
                pass
    
    sndscreen()


def type():
    temp = ''

    pygame.init()
    screen = pygame.display.set_mode((480, 120))
    font = pygame.font.Font(None, 30)

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

        screen.fill((255, 255, 255))
        block = font.render(temp, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()


def recognition():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print('\n')
        while 1:
            r.adjust_for_ambient_noise(source) 
            print("\n------------------------------")
            print("🦎Say something")
            audio=r.listen(source)
            try:
                print("🦈Processing")
                global a
                a = r.recognize_google(audio, language='zh-TW') #zh-CN
                f = open('speech.txt', 'w+')
                f.write(a)
                f.close()
                print(a)
            except speech_recognition.UnknownValueError:
                print("🐤Please say it again")
                # print("oops")
                pass


if __name__ == '__main__':
    # HOST, PORT = "127.0.0.1", 61677
    HOST, PORT = "140.112.73.132", 61677
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

    if os.path.exists('speech.txt'):
        os.remove('speech.txt')
    
    Process(target = type).start()
    Process(target = recognition).start()
    Process(target = video).start()

    # video()
    
    # 3 text (on terminal)
    # Thread(target = send).start()
    # Thread(target = receive).start()

