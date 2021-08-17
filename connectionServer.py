import math
import numpy as np

import constants as const

try:
    import sim
except:
    print('Error import sim. Verify files and settings Coppelia.')
    
class ConnectionInterface(object):
    def __init__(self, radius=7.5, showIm=False):
        self.showImage = showIm
        self.magnetStatus = False
        self.craneStatus = False
        self.connectionStatus = False
        self.distanceClaw = 2*math.pi*radius
        self.currentDistanceClaw = 0  
        self.currentAngleClaw = 0
        self.currentHeightHook = 0

    #Startup Crane
    def init_connection(self, ip = const.IP_SERVER , port = 19997):
        print('Program started - Init Connection')
        
        sim.simxFinish(-1)
        clientID=sim.simxStart(ip, port,True,True,5000,5) # Connect to CoppeliaSim
        if clientID==-1:
            return -1, False
        self.clientID = clientID
        self.connectionStatus = True

        # Get Coppelia Objects ID
        self.boom =  sim.simxGetObjectHandle(clientID,'Atuador_braco',sim.simx_opmode_blocking)[-1]
        self.claw = sim.simxGetObjectHandle(clientID,'Atuador_garra',sim.simx_opmode_blocking)[-1] 
        self.crane = sim.simxGetObjectHandle(clientID,'Atuador_guindaste',sim.simx_opmode_blocking)[-1]
        self.magnet = sim.simxGetObjectHandle(clientID,'suctionPad',sim.simx_opmode_blocking)[-1]
        self.cam = sim.simxGetObjectHandle(clientID,'Vision_sensor',sim.simx_opmode_blocking)[-1]
        self.cam2 = sim.simxGetObjectHandle(clientID,'cam2',sim.simx_opmode_blocking)[-1]
        self.proximity_sensor = sim.simxGetObjectHandle(clientID,'Proximity_sensor',sim.simx_opmode_blocking)[-1]
        self.boomStructure = sim.simxGetObjectHandle(clientID,'Braco',sim.simx_opmode_blocking)[-1]

        self.err_code,_,_ = sim.simxGetVisionSensorImage(clientID,self.cam,0,sim.simx_opmode_streaming)
        self.err_code,_,_ = sim.simxGetVisionSensorImage(clientID,self.cam2,0,sim.simx_opmode_streaming)
        self.status = sim.simxReadProximitySensor(clientID,self.proximity_sensor,sim.simx_opmode_streaming)[1]
        
        return self.clientID, self.connectionStatus
    
    def commandCraneOnOff(self):
        if self.connectionStatus:
            if self.craneStatus:
                sim.simxStopSimulation(self.clientID, sim.simx_opmode_blocking)
            else:
                # Inicia simulacao
                sim.simxStartSimulation(self.clientID, sim.simx_opmode_blocking)
                sim.simxSetJointTargetPosition(self.clientID,self.boom,0,sim.simx_opmode_continuous)
                sim.simxSetJointTargetPosition(self.clientID,self.crane,0,sim.simx_opmode_continuous)
            self.craneStatus = not self.craneStatus
        return self.craneStatus
    
    #Actions
    def actionCrane(self, step):
        if self.craneStatus and self.connectionStatus:
            self.getCurrentHeightHook()
            next_position = self.currentHeightHook + step - 6.6747 # (subtrai offset de altura do gancho)
            sim.simxSetJointTargetPosition(self.clientID,self.crane,next_position,sim.simx_opmode_continuous)
        return self.craneStatus
    
    def actionBoom(self, step):
        if self.craneStatus and self.connectionStatus:
            self.getCurrentAngleClaw()
            next_position = self.currentAngleClaw + step
            sim.simxSetJointTargetPosition(self.clientID,self.boom,degree2radian(next_position),sim.simx_opmode_continuous)
        return self.craneStatus
    
    #Commands
    def commandUp(self, step=1):
        return self.actionCrane(step)
    
    def commandDown(self, step=1):
        return self.actionCrane(step*-1)
    
    def commandLeft(self, step=1):
        return self.actionBoom(step)
    
    def commandRight(self, step=1):
        return self.actionBoom(step*-1)
    
    def commandMagnetOnOff(self):
        if self.craneStatus and self.connectionStatus:
            sim.simxCallScriptFunction(self.clientID,'Base',sim.sim_scripttype_childscript,'AtuadorIma',[],[],[],bytearray(),sim.simx_opmode_blocking)
            self.magnetStatus = not self.magnetStatus
        return self.magnetStatus

    #Status
    def getStatusDist(self):
        if self.craneStatus and self.connectionStatus:
            # Get proximity sensor status
            status = sim.simxReadProximitySensor(self.clientID,self.proximity_sensor,sim.simx_opmode_buffer)[1]
            return status
        return -1
    
    def getMagnetStatus(self):
        return self.magnetStatus
    
    def getStatusDist(self):
        if self.craneStatus and self.connectionStatus:
            # Get proximity sensor status
            status = sim.simxReadProximitySensor(self.clientID,self.proximity_sensor,sim.simx_opmode_buffer)[1]
            return status
        return -1
    
    def getConnectionStatus(self):
        return self.connectionStatus
    
    def getCraneStatus(self):
        return self.craneStatus
    
    #Gets   
    def getCurrentHeightHook(self):
        self.currentHeightHook = sim.simxGetObjectPosition(self.clientID, self.magnet, -1, sim.simx_opmode_blocking)[-1][-1]
        return self.currentHeightHook
    
    def getCurrentAngleClaw(self):
        self.currentAngleClaw = radian2degree(sim.simxGetObjectOrientation(self.clientID,self.boomStructure,-1,sim.simx_opmode_blocking)[-1][-1])
        return self.currentAngleClaw
    
    def getCamImage(self, save = False, number=1):
        image = None
        if self.craneStatus and self.connectionStatus:
            if number == 1:
                err_code,resolution,image = sim.simxGetVisionSensorImage(self.clientID,self.cam,0,sim.simx_opmode_buffer)
            elif number == 2:
                err_code,resolution,image = sim.simxGetVisionSensorImage(self.clientID,self.cam2,0,sim.simx_opmode_buffer)
            if save:
                if err_code == sim.simx_return_ok:
                    img = np.array(image, dtype = np.uint8)
                    img.resize([resolution[0],resolution[1],3])
                    img = np.array(img[::-1], dtype=np.uint8)
                    return img
                else:
                    return None
        return None

# Functions Utils

def radian2degree(angle):
    return 180*angle/math.pi

def degree2radian(angle):
    return math.pi*angle/180

def getAngle360(angle):
    if angle < 0:
        angle += 360
    return angle
