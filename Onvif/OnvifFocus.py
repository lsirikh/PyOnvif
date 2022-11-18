
from Onvif.OnvifFocus import *


class Focus_Continuous():
    Speed = 0.0

class Focus_Absolute():
    Position = 0.0
    Speed = 0.0

class Focus_Relative():
    Distance = 0.0
    Speed = 0.0

class Focus():
    Absolute = None
    Relative = None
    Continuous = None
        
    def setAbsolute(self):
        self.Absolute = Focus_Absolute()
    
    def setRelative(self):
        self.Relative = Focus_Relative()

    def setContinuous(self):
        self.Continuous = Focus_Continuous()

    