import cv2
import threading
import sys
import asyncio

from time import sleep

from Config.JsonService import JsonClass
from Onvif.OnvifService import OnvifClass


class TestOnvif():
    def __init__(self):
        self.setProperty()
        
    def setProperty(self):
        print("OnvifService is now loading...")
        print("Please wait!")
        self.onvif = OnvifClass()

    def read_config_data(self, data):
        self.data = data

    def set_onvif(self):
        self.onvif.setup(self.data["EO"])
    
    def start_thread(self):
        try:
            self.testThread = threading.Thread(target=self.go_test
                                            , name="[Onvif test]")
            self.isTestRun = True
            self.testThread.start()
        except Exception as e:
            self.isTestRun = False
            print("Raised Exception in start_thread : ", e)
        
    def stop_thread(self):
        try:
            if not self.isTestRun:
                return
        
            self.isTestRun = False
            self.testThread.join()
        except Exception as e:
            print("Raised Exception in stop_thread : ", e)

    def go_test(self):
        try:
            print("""
            <<<Explain>>
To control Ptz and Focus with a keyboard
You need to follow the below comment.
All onvif protocol related with Moving was used
as Continuous Way.

Exit(X)

Pan & Tilt - Up(w), Down(s), Left(a), Right(d)
Zoom       - In(r), Out(t)
PTZMove    - Stop(q)
Focus      - In(f), Out(g)  
FocusMove  - Stop(h)
                  """)
            while self.isTestRun:
                key = input('Inert key : ')
                if key == 'w':
                    self.onvif.moveUp_pressDown()
                elif key == 's':
                    self.onvif.moveDown_pressDown()
                elif key == 'a':
                    self.onvif.moveLeft_pressDown()
                elif key == 'd':
                    self.onvif.moveRight_pressDown()
                elif key == 'q':
                    self.onvif.btnReleased()
                elif key == 'r':
                    self.onvif.zoomIn_pressDown()
                elif key == 't':
                    self.onvif.zoomOut_pressDown()
                elif key == 'f':
                    self.onvif.focusIn_pressDown()
                elif key == 'g':
                    self.onvif.focusOut_pressDown()
                elif key == 'h':
                    self.onvif.focus_btnReleased()
                elif key == 'x':
                    self.isTestRun = False
                
        except Exception as e:
            print("Raised Exception in go_test : ", e)

if __name__ == '__main__':
    try:
        
        jConfig = JsonClass()
        data = jConfig.readConfig()
        test = TestOnvif()
        test.read_config_data(data)
        test.set_onvif()
        test.start_thread()
    except Exception as e:
        print("Raised Exception in __main__ : ", e)