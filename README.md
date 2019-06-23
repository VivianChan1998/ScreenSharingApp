# Computer-Networking-Final


功能簡介
----
Server可以傳送螢幕畫面給client，同時server也能用鍵盤或語音輸入文字訊息，和螢幕畫面一起傳送到client端。

如何使用
----
```
$git clone https://github.com/VivianChan1998/ScreenSharingApp.git
$pip install -r requirements.txt
```
Server端：`$python3 server.py`
Client端：`$python3 client.py`

*On Mac OS 10.14:*
Server端：`python3 server.py $OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`
Client端：`python3 client.py $OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

由於使用multiprocessing，在Mac OS 10.14以後必須手動輸入 `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` 指令將限制multiprocessing的設定關掉才能順利執行。也可以在.bash_profile中 `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` 設定。

實作成果
----

### Server端
<p>
  <img width="500" src="https://i.imgur.com/SNhNrOF.jpg">
</p>

<p>
  <img width="500" src="https://i.imgur.com/xFatrL2.jpg">
</p>

右邊的白色視窗顯示的是語音辨識的結果。
下方的白色視窗顯示的是server鍵盤輸入的訊息。

### Client端
<p>
  <img width="500" src="https://i.imgur.com/3gxdqNI.png">
</p>

<p>
  <img width="500" src="https://i.imgur.com/MiNfb49.png">
</p>

畫面顯示的是server端的螢幕畫面，畫面上方的字是server鍵盤輸入的訊息，畫面下方的字則是server語音輸入的訊息。

### Demo Video
[Link 1](https://youtu.be/GyS3F7RrNu0)
<br>
[Link 2](https://youtu.be/OBhFUQ7zE-A)
