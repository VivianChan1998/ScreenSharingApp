import socket
import cv2
import time
from threading import Thread
import pickle
import wx
import numpy as np
# from PIL import ImageGrab     # This does not support linux
import pyscreenshot as ImageGrab
import mss


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


# This is for camera
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
                client.sendall(f.read())
            
            ack = client.recv(128)
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
    def sndscreen():
        # app = wx.App()
        # screen = wx.ScreenDC()
        # size = screen.GetSize()
        while(True):
            #time.sleep(0.01)
            
            # bmp = wx.Bitmap(size[0], size[1])
            # mem = wx.MemoryDC(bmp)
            # mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
            # del mem
            # bmp.SaveFile('screen.jpeg', wx.BITMAP_TYPE_JPEG)

            '''
            #舊方法
            screen = ImageGrab.grab(bbox=(0, 0, 1920, 1200)).resize((1280,800))
            screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1200)).resize((1280,800)))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            cv2.imwrite('screen.jpg', screen, [cv2.IMWRITE_JPEG_QUALITY, 2])
            '''     
            try:
                with mss.mss() as sct:
                    # Part of the screen to capture
                    monitor = {'top': 40, 'left': 0, 'width': 160, 'height': 160}

                    while 'Screen capturing':            
                        # Get raw pixels from the screen, save it to a Numpy array
                        img = np.array(sct.grab(monitor))
                        img = cv2.imencode('.jpg', img)[1].tostring()
                        client.sendall(img)
                #ack = client.recv(128) #先取消ack 為了用兩次recv去防止「傳一次沒有傳到完整圖片但是被ack卡住了」這件事
                #可以再看看能不能加回來，雖然沒有應該不會怎樣吧（？
                
            except:
                pass
        
    sndscreen()
    


if __name__ == '__main__':
    HOST, PORT = "", 61677
    # HOST, PORT = "140.112.226.236", 61677
    # HOST, PORT = "163.13.137.71", 61677
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print('waiting...')
    s.listen(1)

    client, address = s.accept()
    print('%s connected' % str(address))

    # 1 camera
    # sndvideo()

    # 2 screen
    # press "q" to close the screen
    video()

    # 3 text (on terminal)
    # Thread(target = send).start()
    # Thread(target = receive).start()

