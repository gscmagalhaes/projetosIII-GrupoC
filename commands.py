import connectionServer as cs
from connectionServer import ConnectionInterface
import time
import numpy as np
import io
from PIL import Image
import constants as const

class Commands(object):
    def SUBIR(self, window, step, control: ConnectionInterface):
        try:
            old_height = control.getCurrentHeightHook()
            status = control.commandUp(step)
        except:
            status = False 
        if status:
            desired_height = np.clip(old_height + step, float(const.MIN_STEP), float(const.MAX_STEP))
            cnt = 0
            height = control.getCurrentHeightHook()
            while(abs(height - desired_height) > 0.05 and cnt < 200):
                height = control.getCurrentHeightHook()
                cnt+=1
                SetCamImage(window, const.FREQUENCY_UPDATE_DATA / 1000, control)
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima')
        time.sleep(0.5)
    
    def DESCER(self, window, step, control: ConnectionInterface):
        try:
            old_height = control.getCurrentHeightHook()
            status = control.commandDown(step)
        except:
            status = False
            
        if status:
            desired_height = np.clip(old_height - step, float(const.MIN_STEP), float(const.MAX_STEP))
            cnt = 0
            height = control.getCurrentHeightHook()
            while(abs(height - desired_height) > 0.05 and cnt < 200):
                height = control.getCurrentHeightHook()
                cnt+=1
                SetCamImage(window, const.FREQUENCY_UPDATE_DATA / 1000, control)
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima')
            
        time.sleep(0.5)

    def ESQUERDA(self, window, step, control: ConnectionInterface):
        try:
            old_angle = control.getCurrentAngleClaw()
            status = control.commandLeft(step)
        except:
            status = False
        if status:
            desired_angle = cs.getAngle360(old_angle + step)
            cnt = 0
            angle = cs.getAngle360(control.getCurrentAngleClaw())
            while(abs(angle - desired_angle) > 0.1 and cnt < 500):
                angle = cs.getAngle360(control.getCurrentAngleClaw())
                control.getStatusDist()
                cnt+=1
                SetCamImage(window, const.FREQUENCY_UPDATE_DATA / 1000, control)
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima')
        
    def DIREITA(self, window, step, control: ConnectionInterface):
        try:
            old_angle = control.getCurrentAngleClaw()
            step = float(3)
            status = control.commandRight(step)
        except:
            status = False
        if status:
            desired_angle = cs.getAngle360(old_angle - step)
            cnt = 0
            angle = cs.getAngle360(control.getCurrentAngleClaw())
            while(abs(angle - desired_angle) > 0.1 and cnt < 500):
                angle = cs.getAngle360(control.getCurrentAngleClaw())
                cnt+=1
                SetCamImage(window, const.FREQUENCY_UPDATE_DATA / 1000, control)
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima') 
            
    def MAGNET(self, window, control: ConnectionInterface):
        if control.craneStatus and control.connectionStatus:
            status = control.getMagnetStatus()
            if status:
                control.commandMagnetOnOff()
                for _ in np.arange(0.0,control.getCurrentHeightHook(),0.25):
                    SetCamImage(window, const.FREQUENCY_UPDATE_DATA / 1000, control)
            else:
                control.commandMagnetOnOff()
        else:
            print('Sem conexão ou guindaste desligado.')
                       
def SetCamImage(window, camFrequency, connectionLibrary: ConnectionInterface):
    img = connectionLibrary.getCamImage(save=True, number=1)

    if np.any(img):
        image = Image.fromarray(img)
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        camImage = bio.getvalue()
        if camFrequency > 0:
            window.read(camFrequency)
        window['cam1'].update(data=camImage)
