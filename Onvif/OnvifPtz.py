
from Onvif.OnvifPtz import *


class Velocity():
    def __init__(self) -> None:
        self.PanTilt = Velocity_PanTilt()
        self.Zoom = Velocity_Zoom()
    
    
class Velocity_PanTilt():
    x = 0
    y = 0
    
class Velocity_Zoom():
    x = 0
    

