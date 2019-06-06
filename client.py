import cv2
import socket
import time
from PIL import Image
import numpy as np
from random import randint
from multiprocessing import Process


MAX_BUFFER_SIZE = 1000000000

def video():
    # 接收螢幕畫面
    def recscreen():
        while 1:
            # 用多個buffer接收一張圖片
            data = s.recv(MAX_BUFFER_SIZE)     
            for i in range(10):
                data += s.recv(MAX_BUFFER_SIZE)
                
            try:
                # 將收到的資料寫入'save.jpg'
                with open('save.jpg','wb') as f:
                    f.write(data)

                try:
                    # 顯示'save.jpg'（server的螢幕畫面）
                    global frame
                    frame = cv2.imread('save.jpg')
                    cv2.imshow('Server', frame)
                    
                    if cv2.waitKey(100) == ord('q'):
                        cv2.destroyAllWindows()
                        break
                            
                except:
                    pass
                    
            except:
                pass

    recscreen()


if __name__ == "__main__" :
    HOST, PORT = "127.0.0.1", 61677
    # HOST, PORT = "140.112.226.236", 61677
    
    # 建立和server互連的socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('connected to %s' % HOST)

    # 開始Process
    Process(target = video).start()

