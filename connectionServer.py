# implementar conexão com o servidor, envio e recebimento de dados

import math

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
    def init_connection(self, ip = '127.0.0.1' , port = 19997):
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
    
    #Commands
    def commandUp(self, step=1):
        return self.actionCrane(step)
    
    def commandDown(self, step=1):
        print("step commandDown")
        return self.actionCrane(step*-1)
    
    #Status
    def getStatusDist(self):
        if self.craneStatus and self.connectionStatus:
            # Get proximity sensor status
            status = sim.simxReadProximitySensor(self.clientID,self.proximity_sensor,sim.simx_opmode_buffer)[1]
            return status
        return -1
    
    #Gets
    def getConnectionStatus(self):
        return self.connectionStatus
    
    def getCraneStatus(self):
        return self.craneStatus
    
    def getCurrentHeightHook(self):
        self.currentHeightHook = sim.simxGetObjectPosition(self.clientID, self.magnet, -1, sim.simx_opmode_blocking)[-1][-1]
        return self.currentHeightHook

################################################

def connectionStatus():
    # necessário implementar check de conexão
    setOn = 1  # simulação de status 'aguardando conexão'

    if setOn == 0:  # sistema desconectado
        return 'off'
    elif setOn == 1:  # sistema conectado
        return 'on'
    else:  # sistema aguardadndo conexão
        return 'wait'

# função de check de status do guincho (retorno soble o acoplamento dos containers)


def getObjectStatus():
    # necessário implementar check de captação de objetos
    holdOn = 2  # simulação de status 'gancho ocupado'

    if holdOn == 0:  # gancho livre
        return 'free'
    elif holdOn == 1:  # gancho ocupado
        return 'hold'
    else:  # ganho tentando coletar objeto
        return 'tring'
