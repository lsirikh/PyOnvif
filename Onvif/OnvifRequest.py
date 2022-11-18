import hashlib
import os
import base64
from datetime import datetime
import socket
import requests

class OnvifRequest():
    def __init__(self):
        print("OnvifRequest Class was created")
    
    def __init__(self, username, password):
        print("OnvifRequest Class was created with createRequest")
        self.createRequest(username, password)
        
    
    def createRequest(self, id, pw):
        try:
            self.username = id
            self.password = pw

        except Exception as e:
            print("Raised Exception in createRequest of OnvifRequest : ", e)
    
    def requestXml(self, body):
        template = """
                    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
                        {header}
                        {body}
                    </s:Envelope>
                    """
        req_body = template.format(header = self.createHeaderXml(),
                                   body = body)
        
        return req_body
    
    def createHeaderXml(self):
        created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

        raw_nonce = os.urandom(20)
        nonce = base64.b64encode(raw_nonce)

        sha1 = hashlib.sha1()
        sha1.update(raw_nonce + created.encode('utf8') + self.password.encode('utf8'))
        raw_digest = sha1.digest()
        digest = base64.b64encode(raw_digest)
        
        template = """
                    <s:Header>
                        <Security s:mustUnderstand="1" xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                            <UsernameToken>
                                <Username>{username}</Username>
                                <Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{digest}</Password>
                                <Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</Nonce>
                                <Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">{created}</Created>
                            </UsernameToken>
                        </Security>
                    </s:Header>
                    """
        req_header = template.format(username=self.username, 
                                   nonce=nonce.decode('utf8'), 
                                   created=created, 
                                   digest=digest.decode('utf8'))
        
        return req_header
    
    
    def ptzContinuousXml(self, request):
        template = """
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <ContinuousMove xmlns="http://www.onvif.org/ver20/ptz/wsdl">
                            <ProfileToken>{profile_token}</ProfileToken>
                            <Velocity>
                                <PanTilt x="{pan}" y="{tilt}" xmlns="http://www.onvif.org/ver10/schema"/>
                                <Zoom x="{zoom}" xmlns="http://www.onvif.org/ver10/schema"/>
                            </Velocity>
                        </ContinuousMove>
                    </s:Body>
                    """
        req_body = template.format(profile_token = request.ProfileToken, 
                                   pan = request.Velocity.PanTilt.x, 
                                   tilt = request.Velocity.PanTilt.y,
                                   zoom = request.Velocity.Zoom.x)
        return req_body
    
    
    def ptzStopXml(self, request):
        template = """
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <Stop xmlns="http://www.onvif.org/ver20/ptz/wsdl">
                            <ProfileToken>{profile_token}</ProfileToken>
                            <PanTilt>{panTilt}</PanTilt>
                            <Zoom>{zoom}</Zoom>
                        </Stop>
                    </s:Body>
                    """
        req_body = template.format(profile_token = request.ProfileToken, 
                                   panTilt = "true", 
                                   zoom = "true")    
        
        return req_body
    
    def ContinuousMove(self, request):
        try:
            body = self.ptzContinuousXml(request)
            self.sendRequest(body, self.ptz_xaddr)
            #req_body = self.requestXml(body)
            #conn = requests.post(self.ptz_xaddr, req_body)
        except Exception as e:
            print("Raised an exception during ContinuousMove : ", e)
        
    def Stop(self, request):
        try:
            body = self.ptzStopXml(request)
            self.sendRequest(body, self.ptz_xaddr)
            #req_body = self.requestXml(body)
            #conn = requests.post(self.ptz_xaddr, req_body)
        except Exception as e:
            print("Raised an exception during Stop : ", e)
        
        
    def setPtzXaddr(self, ptz):
        self.ptz_xaddr = ptz.xaddr
        
    def focusContinuousXml(self, request):
        template = """
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <Move xmlns="http://www.onvif.org/ver20/imaging/wsdl">
                            <VideoSourceToken>{token}</VideoSourceToken>
                            <Focus>
                                <Continuous xmlns="http://www.onvif.org/ver10/schema">
                                    <Speed>{speed}</Speed>
                                </Continuous>
                            </Focus>
                        </Move>
                    </s:Body>
                    """
        req_body = template.format(token = request.VideoSourceToken, 
                                   speed = request.Focus.Continuous.Speed)
        return req_body
    
    
    def focusStopXml(self, request):
        template = """
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <Stop xmlns="http://www.onvif.org/ver20/imaging/wsdl">
                            <VideoSourceToken>{token}</VideoSourceToken>
                        </Stop>
                    </s:Body>
                    """
        req_body = template.format(token = request.VideoSourceToken)    
        
        return req_body
    
    def focusContinuousMove(self, request):
        try:
            body = self.focusContinuousXml(request)
            self.sendRequest(body, self.imaging_xaddr)
            #req_body = self.requestXml(body)
            #conn = requests.post(self.ptz_xaddr, req_body)
        except Exception as e:
            print("Raised an exception during focusContinuousMove : ", e)
        
        
    def focusStop(self, request):
        try:
            body = self.focusStopXml(request)
            self.sendRequest(body, self.imaging_xaddr)
            #req_body = self.requestXml(body)
            #conn = requests.post(self.ptz_xaddr, req_body)
        except Exception as e:
            print("Raised an exception during focusStop : ", e)
        
    def setImagingXaddr(self, imaging):
        self.imaging_xaddr = imaging.xaddr
        
    def sendRequest(self, body, xaddr):
        try:
            req_body = self.requestXml(body)
            conn = requests.post(xaddr, req_body)
        except Exception as e:
            print("Raised an exception during sendRequest : ", e)
        