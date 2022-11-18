from onvif import *
import zeep
# from zeep import Client, Settings
# import asyncio
# import json
from Onvif.OnvifRequest import OnvifRequest
from Onvif.OnvifPtz import *
from Onvif.OnvifFocus import *
from time import sleep, time


import types

class OnvifClass():
    def __init__(self) -> None:
        print("Created OnvifCalss!!")
        self.setProperties()
    
    def setProperties(self):
        self.isOnvifCamera = False
        self.isSetMediaService = False
        self.isSetPtzService = False
        self.isSetAnalyticService = False
        self.isSetDeviceIOService = False
        self.isSetDeviceMgmtService = False
        self.isSetImagingService = False
        self.isSetReplayService = False
        self.isSetReceiverService = False
        self.isSetEventsService = False
        self.isSetRecordingService = False
        self.isSetPullpointService = False
        self.isSetOnvifService = False
        
        self.isSetRequestStop = False
        self.isSetRequestCont = False
        
        self.XMAX = 1
        self.XMIN = -1
        self.YMAX = 1
        self.YMIN = -1
        self.FMAX = 0.5
        self.FMIN = -0.5

        self.__onvifPtzProtocol = False
        self.__onvifFocusProtocol = False
    
    def setup(self, data):
        try:
            ipAddress = data["onvif"]["ip_address"]
            port = str(data["onvif"]["port"])
            id = data["onvif"]["id"]
            pw = data["onvif"]["password"]
            # self.mycam = ONVIFCamera(ipAddress, port, id, pw)
            # self.onvifRequest = OnvifRequest(id, pw)
            self.setupOnvifCamera(ipAddress, port, id, pw)
            self.createServices()
            self.setupFocusOperation()
            self.setupPtzOperation()
        except Exception as e:
            print("Exception raised when parsing Data in setup : ", e)
       
        try:
            # Get zeep_pythonvalue
            zeep.xsd.simple.AnySimpleType.pythonvalue = self.zeep_pythonvalue
        except Exception as e:
            print("Raised an exception during zeep_pythonvalue : ", e)
    
    # async def setup_async(self, data):
    #     try:
    #         ipAddress = data["onvif"]["ip_address"]
    #         port = str(data["onvif"]["port"])
    #         id = data["onvif"]["id"]
    #         pw = data["onvif"]["password"]
    #         await asyncio.wait([
    #             self.setupOnvifCamera(ipAddress, port, id, pw),
    #             self.createServices(),
    #             self.setupFocusOperation(),
    #             self.setupPtzOperation(),
    #         ])
            
    #     except Exception as e:
    #         print("Exception raised when parsing Data in setup_async : ", e)
       
    #     try:
    #         # Get zeep_pythonvalue
    #         zeep.xsd.simple.AnySimpleType.pythonvalue = self.zeep_pythonvalue
    #     except Exception as e:
    #         print("Raised an exception during zeep_pythonvalue : ", e)
    
    def setupOnvifCamera(self, ipAddress, port, id, pw):
        try:
            self.mycam = ONVIFCamera(ipAddress, port, id, pw, wsdl_dir="./wsdl")
            # Alternative Request for SOAP onvif operation
            self.onvifRequest = OnvifRequest(id, pw) 
            self.isOnvifCamera = True
            #await self.mycam.update_xaddrs()
            self.services = self.mycam.use_services_template
        except Exception as e:
            print("Exception raised in setupOnvifCamera : ", e)
    
    def setupMedia(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create media service object
            self.media = self.mycam.create_media_service()
            self.isSetMediaService = True
            

        except Exception as e:
            print("Exception raised in setupMedia : ", e)
            
    def setupAnalytics(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create analytics service object
            self.analytics = self.mycam.create_analytics_service()
            self.isSetAnalyticService = True
            self.analytics_capabilities = self.analytics.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupAnalytics : ", e)
            
    def setupDeviceIO(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create deviceIO service object
            self.deviceIO = self.mycam.create_deviceio_service()
            self.isSetDeviceIOService = True
            self.deviceIO_capabilities = self.deviceIO.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceIO : ", e)
            
    def setupDeviceMgmt(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create DeviceMgmt service object
            self.deviceMgmt = self.mycam.create_devicemgmt_service()
            self.isSetDeviceMgmtService = True
            self.deviceMgmt_capabilities = self.deviceMgmt.GetCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceMgmt : ", e)
    
    def setupImaging(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create imaging service object
            self.imaging = self.mycam.create_imaging_service()
            self.isSetImagingService = True
            self.imaging_capabilities = self.imaging.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceIO : ", e)
    
    def setupReplay(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create replay service object
            self.replay = self.mycam.create_replay_service()
            self.isSetReplayService = True
            self.replay_capabilities = self.replay.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupReplay : ", e)
    
    def setupReceiver(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create receiver service object
            self.receiver = self.mycam.create_receiver_service()
            self.isSetReceiverService = True
            self.receiver_capabilities = self.receiver.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupReceiver : ", e)
    
    def setupEvents(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create event service object
            self.events = self.mycam.create_events_service()
            self.isSetEventsService = True
            self.events_capabilities = self.events.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupEvent : ", e)
    
    def setupRecording(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.recording = self.mycam.create_recording_service()
            self.isSetRecordingService = True
            self.recording_capabilities = self.recording.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupRecording : ", e)
            
    def setupPullpoint(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.pullpoint = self.mycam.create_pullpoint_service()
            self.isSetPullpointService = True
            self.pullpoint_capabilities = self.pullpoint.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupPullpoint : ", e)
    
    def setupOnvif(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.onvif = self.mycam.create_onvif_service()
            self.isSetOnvifService = True
            self.onvif_capabilities = self.onvif.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupOnvif : ", e)
    
    def setupPtz(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create ptz service object
            self.ptz = self.mycam.create_ptz_service()
            self.isSetPtzService = True
            self.ptz_capabilities = self.ptz.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupPtz : ", e)
       
    def createServices(self):
        for key, value in self.services.items():
            service = key.lower()
            #print(self.mycam.xaddrs)
            #print(service, value)
            if service == 'devicemgmt':
                self.setupDeviceMgmt()
            elif service == 'ptz':
                self.setupPtz()
            elif service == 'media':
                self.setupMedia()
                self.getMediaProfiles()
            elif service == 'imaging':
                self.setupImaging()
            elif service == 'events':
                self.setupEvents
            elif service == 'analytics':
                self.setupAnalytics()
            elif service == 'deviceio':
                self.setupDeviceIO()
            elif service == 'recording':
                self.setupRecording()
            elif service == 'receiver':
                self.setupReceiver()
            elif service == 'replay':
                self.setupReplay()
            elif service == 'onvif':
                self.setupOnvif()
            elif service == 'pullpoint':
                self.setupPullpoint()
    
        self.getVideoSources()
    
    def getMediaProfiles(self):
        try:
            if not self.isSetMediaService:
                return
            
            # Get target profile
            self.media_profiles = self.media.GetProfiles()
            #print(self.media_profiles)
            self.media_profile = self.media.GetProfiles()[0]
            
        except Exception as e:
            print("Raised an exception during getMediaProfiles : ", e)
    
    def getVideoSources(self):
        try:
            if not self.isSetMediaService:
                return
            
            video_sources = self.media.GetVideoSources()
            self.vsource = video_sources[0]
            self.checkVideoSources(video_sources)
            
        except Exception as e:
            print("Raised an exception during getVideoSources : ", e)
    
    def setImageProperties(self):
        try:
            if self.vsource is None:
                return
                
            self.imaging_option = self.getImagingOption(self.vsource.token)
            self.imaging_status = self.getImagingStatus(self.vsource.token)
            self.imaging_moveOption = self.getImagingMoveOption(self.vsource.token)
            self.imaging_settings = self.getImagingSettings(self.vsource.token)
                        
        except Exception as e:
            print("Raised an exception during setImageProperties : ", e)
    
    def checkVideoSources(self, video_sources):
        try:
            for vsource in video_sources:
                if vsource.token is not None:
                    print(f"vsource token : {vsource.token}")
                
                if vsource.Resolution is not None:
                    print(f"vsource resolution : {vsource.Resolution.Width}x{vsource.Resolution.Height}")

                if vsource.Framerate is not None:
                    print(f"vsource frame : {vsource.Framerate}")
                
                imaging_option = self.getImagingOption(vsource.token)
                
                if vsource.Imaging is not None :
                    self.checkBrightness(vsource.Imaging, imaging_option)                        
                    self.checkColorSaturation(vsource.Imaging, imaging_option)                        
                    self.checkContrast(vsource.Imaging, imaging_option)                        
                    self.checkExposure(vsource.Imaging, imaging_option)                        
                    self.checkFocus(vsource.Imaging, imaging_option)                        
                    self.checkIrCutFilter(vsource.Imaging, imaging_option)                        
                    self.checkSharpness(vsource.Imaging, imaging_option)                        
                    self.checkWhiteBalance(vsource.Imaging, imaging_option)                        
                    self.checkWideDynamicRange(vsource.Imaging, imaging_option)                        
                        
        except Exception as e:
            print("Raised an exception during checkVideoSources : ", e)
    
    def checkBrightness(self, imaging, imaging_option):
        try:
            if imaging.Brightness is not None :
                print(f"Imaging Brightness : {imaging.Brightness}", end="")
            if imaging_option.Brightness is not None :
                print(f"({imaging_option.Brightness.Min}/{imaging_option.Brightness.Max})")
            else:
                print()
        except Exception as e:
            print("Raised an exception during checkBrightness : ", e)
    
    def checkColorSaturation(self, imaging, imaging_option):
        try:
            if imaging.ColorSaturation is not None :
                print(f"Imaging ColorSaturation : {imaging.ColorSaturation}", end="")
            if imaging_option.ColorSaturation is not None :
                print(f"({imaging_option.ColorSaturation.Min}/{imaging_option.ColorSaturation.Max})")
            else:
                print()
        except Exception as e:
            print("Raised an exception during checkColorSaturation : ", e)
    
    def checkContrast(self, imaging, imaging_option):
        try:
            if imaging.Contrast is not None :
                print(f"Imaging Contrast : {imaging.Contrast}", end="")
            if imaging_option.Contrast is not None :
                print(f"({imaging_option.Contrast.Min}/{imaging_option.Contrast.Max})")
            else:
                print()
        except Exception as e:
            print("Raised an exception during checkContrast : ", e)
    
    def checkExposure(self, imaging, imaging_option):
        try:
            if imaging.Exposure is not None :
                print("Imaging Iris(Mode) : ", imaging.Exposure.Mode)
                print("Imaging Iris(ExposureTime) : ", imaging.Exposure.ExposureTime)
                print("Imaging Iris(Gain) : ", imaging.Exposure.Gain)
                print("Imaging Iris(Iris) : ", imaging.Exposure.Iris)
                print("Imaging Iris(MaxExposureTime) : ", imaging.Exposure.MaxExposureTime)
                print("Imaging Iris(MinExposureTime) : ", imaging.Exposure.MinExposureTime)
                print("Imaging Iris(MaxGain) : ", imaging.Exposure.MaxGain)
                print("Imaging Iris(MinGain) : ", imaging.Exposure.MinGain)
                print("Imaging Iris(MaxIris) : ", imaging.Exposure.MaxIris)
                print("Imaging Iris(MinIris) : ", imaging.Exposure.MinIris)
                print("Imaging Iris(Mode) : ", imaging.Exposure.Mode)
                print("Imaging Iris(Priority) : ", imaging.Exposure.Priority)
            
        except Exception as e:
            print("Raised an exception during checkExposure : ", e)
    
    def checkFocus(self, imaging, imaging_option):
        try:
            if imaging.Focus is not None :
                print("Imaging Focus(AutoFocusMode) : ", imaging.Focus.AutoFocusMode)
                print("Imaging Focus(NearLimit) : ", imaging.Focus.NearLimit)
                print("Imaging Focus(FarLimit) : ", imaging.Focus.FarLimit)
                print("Imaging Focus(DefaultSpeed) : ", imaging.Focus.DefaultSpeed)
            
        except Exception as e:
            print("Raised an exception during checkFocus : ", e)
    
    def checkIrCutFilter(self, imaging, imaging_option):
        try:
            if imaging.IrCutFilter is not None :
                print(f"Imaging IrCutFilter(Mode) : {imaging.Sharpness}")
        except Exception as e:
            print("Raised an exception during checkIrCutFilter : ", e)
            
    def checkSharpness(self, imaging, imaging_option):
        try:
            if imaging.Sharpness is not None :
                print(f"Imaging Sharpness : {imaging.Sharpness}", end="")
            if imaging_option.Sharpness is not None :
                print(f"({imaging_option.Sharpness.Min}/{imaging_option.Sharpness.Max})")
            else:
                print()
        except Exception as e:
            print("Raised an exception during checkSharpness : ", e)
            
    def checkWhiteBalance(self, imaging, imaging_option):
        try:
            if imaging.WhiteBalance is not None :
                print("Imaging WhiteBalance(Mode) : ", imaging.WhiteBalance.Mode)
                print("Imaging WhiteBalance(CrGain) : ", imaging.WhiteBalance.CrGain)
                print("Imaging WhiteBalance(CbGain) : ", imaging.WhiteBalance.CbGain)
        except Exception as e:
            print("Raised an exception during checkWhiteBalance : ", e)
            
    def checkWideDynamicRange(self, imaging, imaging_option):
        try:
            if imaging.WideDynamicRange is not None :
                print("Imaging WideDynamicRange(Mode) : ", imaging.WideDynamicRange.Mode)
                print(f"Imaging WideDynamicRange(Level) : {imaging.WideDynamicRange.Level}", end="")
            if imaging_option.WideDynamicRange is not None :
                print(f"({imaging_option.WideDynamicRange.Level.Min}/{imaging_option.WideDynamicRange.Level.Max})")
            else:
                print(f"")
        except Exception as e:
            print("Raised an exception during checkWideDynamicRange : ", e)
    
    def getImagingOption(self, token):
        try:
            if not self.isSetImagingService:
                return
            
            return self.imaging.GetOptions(token)
        except Exception as e:
            print("Raised an exception during getImagingOption : ", e)
    
    def getImagingStatus(self, token):
        try:
            if not self.isSetImagingService:
                return
            
            return self.imaging.GetStatus(token)
        except Exception as e:
            print("Raised an exception during getImagingStatus : ", e)
    
    def getImagingMoveOption(self, token):
        try:
            if not self.isSetImagingService:
                return
            
            return self.imaging.GetMoveOptions(token)
        except Exception as e:
            print("Raised an exception during getImagingMoveOption : ", e)
    
    def getImagingSettings(self, token):
        try:
            if not self.isSetImagingService:
                return
            
            return self.imaging.GetImagingSettings(token)
        except Exception as e:
            print("Raised an exception during getImagingSettings : ", e)
    
    def setupFocusOperation(self):
        try:
            self.setImageProperties()
            self.setFocusMax()
            self.createFocusContReq()
            self.createFocusStopReq()
            self.focusContTest()
        except Exception as e:
            print("Raised an exception during setupFocusOperation : ", e)
    
    def setFocusMax(self):
        try:
            if self.imaging_moveOption.Continuous is None :
                return
            self.FMAX = self.imaging_moveOption.Continuous.Speed.Max
            self.FMIN = self.imaging_moveOption.Continuous.Speed.Min
        except Exception as e:
            print("Raised an exception during setFocusMax : ", e)
    
    def setFocusContVelocity(self):
        try:
            focus = Focus()
            focus.setContinuous()
            self.request_focus_continuousMove.Focus = focus
            #self.request_focus_continuousMove.Focus = self.imaging.GetStatus({'VideoSourceToken': self.vsource.token}).Position
            #self.request_ptz_continuousMove.Velocity.PanTilt.space = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            #self.request_ptz_continuousMove.Velocity.Zoom.space = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI
        except Exception as e:
            print("Raised an exception during setFocusContVelocity : ", e)
    
    def setFocusStopStatus(self):
        try:
            self.request_focus_stop.VideoSourceToken  = self.vsource.token
        except Exception as e:
            print("Raised an exception during setFocusStopStatus : ", e)
    
    def createFocusContReq(self):
        try:
            #Set Continuous request
            #test = self.imaging.get_type('Move')
            self.request_focus_continuousMove = self.imaging.create_type('Move')
            self.request_focus_continuousMove.VideoSourceToken  = self.vsource.token
            self.request_focus_continuousMove.Focus = {"Continuous": {"Speed": 0.0}}
            #self.setFocusContVelocity()
            
        except Exception as e:
            print("Raised an exception during createFocusContReq : ", e)
    
    def createFocusStopReq(self):
        try:
            #Set Ptz stop
            self.request_focus_stop = self.imaging.create_type('Stop')
            self.request_focus_stop.VideoSourceToken  = self.vsource.token
            self.setFocusStopStatus()
            
        except Exception as e:
            print("Raised an exception during createFocusStopReq : ", e)
    
    def focusContTest(self):
        try:
            self.request_focus_continuousMove.Focus['Continuous']['Speed'] = 0.5
            #self.request_focus_continuousMove.Focus.Continuous.Speed = 0.5
            
            #self.onvifRequest.focusContinuousMove(self.request_focus_continuousMove)
            response = self.imaging.Move(self.request_focus_continuousMove)
            sleep(1)
            response = self.imaging.Stop(self.request_focus_stop)
            self.__onvifFocusProtocol = True
        except Exception as e:
            self.onvifRequest.setImagingXaddr(self.imaging)
            focus = Focus()
            focus.setContinuous()
            self.request_focus_continuousMove.Focus = focus
            self.__onvifFocusProtocol = False
            print("Raised an exception during focusContTest : ", e)
            
    
    def setupPtzOperation(self):
        try:
            self.getPTZConfigOption()
            self.setPTZMax()
            self.createPTZContReq()
            self.createPTZStopReq()
            self.setPTZContVelocity()
            self.ptzContTest()
        except Exception as e:
            print("Raised an exception during setupPtzOperation : ", e)
    
    def getPTZConfigOption(self):
        try:
            # Get PTZ configuration options for getting continuous move range
            self.request_ptzOption = self.ptz.create_type('GetConfigurationOptions')
            self.request_ptzOption.ConfigurationToken = self.media_profile.PTZConfiguration.token
            self.ptz_configuration_options = self.ptz.GetConfigurationOptions(self.request_ptzOption)
        except Exception as e:
            print("Raised an exception during getPTZConfigOption : ", e)
    
    def createPTZContReq(self):
        try:
            
            #Set Continuous request
            self.request_ptz_continuousMove = self.ptz.create_type('ContinuousMove')
            self.request_ptz_continuousMove.ProfileToken = self.media_profile.token
            self.setPTZContVelocity()
        except Exception as e:
            print("Raised an exception during createPTZContReq : ", e)
            
    def createPTZStopReq(self):
        try:
            #Set Ptz stop
            self.request_ptz_stop = self.ptz.create_type('Stop')
            self.isSetRequestStop = True
            self.setPTZStopStatus()
            
        except Exception as e:
            print("Raised an exception during createPTZStopReq : ", e)

    def setPTZStopStatus(self):
        try:
            self.request_ptz_stop.PanTilt = True
            self.request_ptz_stop.Zoom = True
            self.request_ptz_stop.ProfileToken = self.media_profile.token
        except Exception as e:
            print("Raised an exception during setPTZStopStatus : ", e)
            
    def setPTZContVelocity(self):
        try:
            if self.request_ptz_continuousMove.Velocity is None:
                raise NotImplementedError()
            
            self.request_ptz_continuousMove.Velocity = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position
            #self.request_ptz_continuousMove.Velocity.PanTilt.space = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            #self.request_ptz_continuousMove.Velocity.Zoom.space = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI
        except NotImplementedError as e:
            self.request_ptz_continuousMove.Velocity  = Velocity()
            print("self.ptz_configuration_options is empty")
        except Exception as e:
            print("Raised an exception during setPTZContVelocity : ", e)

    def setPTZMax(self):
        # Get range of pan and tilt
        # NOTE: X and Y are velocity vector
        try:
            if self.ptz_configuration_options.Spaces is None:
                raise NotImplementedError()
            
            self.XMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
            self.XMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
            self.YMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
            self.YMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
        except NotImplementedError as e:
            print("self.ptz_configuration_options is empty")
        except Exception as e:
            print("Raised an exception during setMax : ", e)
    
    def ptzContTest(self):
        try:
            self.ptz.Stop(self.request_ptz_stop)
            self.__onvifPtzProtocol = True
            
        except Exception as e:
            self.onvifRequest.setPtzXaddr(self.ptz)
            self.__onvifPtzProtocol = False
            print("Raised an exception during ptzContTest : ", e)
       
    def getRtspUri(self):
        try:
            self.obj = self.media.create_type('GetStreamUri')
            self.obj.ProfileToken = self.media_profile.token
            self.obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
            #print(self.media.GetStreamUri(self.obj)["Uri"])
            return self.media.GetStreamUri(self.obj)["Uri"]
        
        except Exception as e:
            print("Raised an exception during getRtspUri : ", e)
            
    
    def getStreamingUrl(self):
        print(self.request_ptz_continuousMove)
        
    
    def zeep_pythonvalue(self, xmlvalue):
        return xmlvalue

    def focusIn_pressDown(self):
        try:
            # Start continuous move
            if self.__onvifFocusProtocol:
                self.request_focus_continuousMove.Focus['Continuous']['Speed'] = 0.5
                self.imaging.Move(self.request_focus_continuousMove)
            else:
                self.request_focus_continuousMove.Focus.Continuous.Speed = 0.5
                self.onvifRequest.focusContinuousMove(self.request_focus_continuousMove)
        except Exception as e:
            print("Raised Exception in focusIn_pressDown : ", e)
    
    def focusOut_pressDown(self):
        try:
            # Start continuous move
            if self.__onvifFocusProtocol:
                self.request_focus_continuousMove.Focus['Continuous']['Speed'] = -0.5
                self.imaging.Move(self.request_focus_continuousMove)
            else:
                self.request_focus_continuousMove.Focus.Continuous.Speed = -0.5
                self.onvifRequest.focusContinuousMove(self.request_focus_continuousMove)
        except Exception as e:
            print("Raised Exception in focusOut_pressDown : ", e)
    
    def focus_btnReleased(self):
        try:
            # Start continuous move
            if self.__onvifFocusProtocol:
                self.imaging.Stop(self.request_focus_stop)
            else:
                self.onvifRequest.focusStop(self.request_focus_stop)
        except Exception as e:
            print("Raised Exception in focus_btnReleased : ", e)
            
    def moveUp_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.y = self.YMAX
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            print("Raised Exception in moveUp_pressDonw : ", e)
            
        
    def moveDown_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.y = self.YMIN
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            
            print("Raised Exception in moveDown_pressDown : ", e)
            
    
    def moveRight_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.x = self.XMAX
            self.request_ptz_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            print("Raised Exception in moveRight_pressDonw : ", e)
            
    
    def moveLeft_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.x = self.XMIN
            self.request_ptz_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            print("Raised Exception in moveLeft_pressDonw : ", e)
            
    
    def zoomOut_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = -1
            self.request_ptz_continuousMove.Velocity.PanTilt.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            print("Raised Exception in zoomOut_pressDown : ", e)
            
        
    def zoomIn_pressDown(self):
        try:
            self.request_ptz_continuousMove.Velocity.Zoom.x = 1
            self.request_ptz_continuousMove.Velocity.PanTilt.x = 0
            self.request_ptz_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_ptz_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_ptz_continuousMove)
        except Exception as e:
            print("Raised Exception in zoomUp_pressDown : ", e)
            
    
    def btnReleased(self):
        try:
            #self.ptz.Stop({'ProfileToken': self.request.ProfileToken})
            if self.__onvifPtzProtocol:
                self.ptz.Stop(self.request_ptz_stop)
            else:
                self.onvifRequest.Stop(self.request_ptz_stop)
        except Exception as e:
            print("Raised Exception in btnReleased : ", e)
            