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


def video():
    font = ImageFont.truetype('SimSun-Bold.ttf', 28)

    # 傳送螢幕畫面
    def sndscreen():
        resolution = 20     # 影像畫質

        while(True):
            # 開啟要顯示的鍵盤輸入訊息
            try:
                f = open('message.txt')
                message = f.read()
                f.close()
            except:
                message = ""
            # 開啟要顯示的語音輸入訊息
            try:
                f = open('speech.txt')
                speech = f.read()
                f.close()
            except:
                speech = ""
            
            # 螢幕截圖
            screen = ImageGrab.grab(bbox=(640, 400, 1920, 1200)).resize((640, 400))
            # 在圖片上加入語音輸入的訊息（speech）
            draw = ImageDraw.Draw(screen)
            draw.text((10, 350), speech, font = font, fill = (51, 153, 255, 1))

            screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)
            # 在圖片上加入鍵盤輸入的訊息（message）
            cv2.putText(screen, message, (10, 40), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,153,51), 2, cv2.LINE_AA)
            # 將圖片儲存為'screen.jpg'
            cv2.imwrite('screen.jpg', screen, [cv2.IMWRITE_JPEG_QUALITY, resolution])
            
            try:
                start = time.time()
                # 將'screen.jpg'傳送給client
                with open('screen.jpg','rb') as f:
                    client.sendall(f.read())

                # 若圖片傳送時間超過1e-3秒，降低圖片畫質
                sample = time.time()- start
                if sample > 1e-3:
                    resolution = 10
                else:
                    resolution = 20
                
            except:
                pass
    
    sndscreen()


# 鍵盤輸入訊息
def type():
    temp = ''
    # 開新的視窗
    pygame.init()
    screen = pygame.display.set_mode((480, 120))
    font = pygame.font.Font(None, 30)

    while True:
        # 讀取鍵盤輸入，將結果寫入'message.txt'
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

        # 將輸入的訊息顯示在視窗中
        screen.fill((255, 255, 255))
        block = font.render(temp, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()


# 語音輸入訊息
def recognition():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print('\n')
        while 1:
            # 讀取麥克風輸入
            r.adjust_for_ambient_noise(source) 
            print("\n------------------------------")
            print("🦎Say something")
            audio=r.listen(source)
            try:
                # 執行語音辨識，將結果寫入'speech.txt'
                print("🦈Processing")
                global a
                a = r.recognize_google(audio, language='zh-TW') #zh-CN
                f = open('speech.txt', 'w+')
                f.write(a)
                f.close()
                print(a)
            except speech_recognition.UnknownValueError:
                # 無法辨識
                print("🐤Please say it again")
                pass


if __name__ == '__main__':
    HOST, PORT = "127.0.0.1", 61677
    # HOST, PORT = "140.112.226.236", 61677
    
    # 建立和client互連的socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print('waiting...')
    s.listen(1)

    client, address = s.accept()
    print('%s connected' % str(address))

    if os.path.exists('message.txt'):
        os.remove('message.txt')

    if os.path.exists('speech.txt'):
        os.remove('speech.txt')
    
    # 開始多個Process
    Process(target = type).start()
    Process(target = recognition).start()
    Process(target = video).start()

