import PySimpleGUI as sg
import checkAction as check
import connectionServer as cs
from connectionServer import ConnectionInterface
import time
import numpy as np

class Commands(object):
    def SUBIR(self, control: ConnectionInterface):
        try:
            old_height = control.getCurrentHeightHook()
            step = 3 #np.clip(float(cod),0.0,6.6747)
            status = control.commandUp(step)
        except:
            status = False 
        if status:
            desired_height = np.clip(old_height + step, 0.0, 6.6747)
            cnt = 0
            height = control.getCurrentHeightHook()
            while(abs(height - desired_height) > 0.05 and cnt < 200):
                height = control.getCurrentHeightHook()
                cnt+=1
                # im1 = control.getCamImage(save=True,number=1)
                # im2 = control.getCamImage(save=True,number=2)
                # if im1 is not None:
                #     self.pixmap = QtGui.QPixmap(im1)
                #     self.pixmap = self.pixmap.scaled(220,220)
                #     self.view.setPixmap(self.pixmap)
                # if im2 is not None:
                #     self.pixmap2 = QtGui.QPixmap(im2)
                #     self.pixmap2 = self.pixmap2.scaled(220,220)
                #     self.view2.setPixmap(self.pixmap2)
                dist = control.getStatusDist()
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima')
        time.sleep(0.5)
        dist = control.getStatusDist()
    
    def DESCER(self, control: ConnectionInterface):
        try:
            old_height = control.getCurrentHeightHook()
            step = 3
            status = control.commandDown(step)
        except:
            status = False
            
        if status:
            desired_height = np.clip(old_height - step, 0.0, 6.6747)
            cnt = 0
            height = control.getCurrentHeightHook()
            while(abs(height - desired_height) > 0.05 and cnt < 200):
                #app.processEvents()
                height = control.getCurrentHeightHook()
                cnt+=1
                # im1 = control.getCamImage(save=True,number=1)
                # im2 = control.getCamImage(save=True,number=2)
                # if im1 is not None:
                #     self.pixmap = QtGui.QPixmap(im1)
                #     self.pixmap = self.pixmap.scaled(220,220)
                #     self.view.setPixmap(self.pixmap)
                # if im2 is not None:
                #     self.pixmap2 = QtGui.QPixmap(im2)
                #     self.pixmap2 = self.pixmap2.scaled(220,220)
                #     self.view2.setPixmap(self.pixmap2)
                dist = control.getStatusDist()
        else:
            print('Não pode ser alterado por não estar ligado ou Falta valor de passo no campo acima')
            time.sleep(0.5)
            dist = control.getStatusDist()

# envio de comandos para o Guindaste
def comandos(sentido, page):
    if sentido == "SUBIR":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM ERGUER O GUINDASTE/GUINCHO!
        check.buttonAction("Você clicou em 'SUBIR'!", page)

    if sentido == "DESCER":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM ABAIXAR O GUINDASTE/GUINCHO!
        check.buttonAction("Você clicou em 'DESCER'!", page)

    if sentido == "ESQUERDA":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM GIRAR O GUINDASTE PARA A ESQUERDA!
        check.buttonAction("Você clicou em 'ESQUERDA'!", page)

    if sentido == "DIREITA":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM GIRAR O GUINDASTE PARA A DIREITA!
        check.buttonAction("Você clicou em 'DIREITA'!", page)

    if sentido == "AVANÇAR":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM AVANÇAR O GUINCHO!
        check.buttonAction("Você clicou em 'AVANÇAR'!", page)

    if sentido == "RECUAR":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM RECUAR O GUINCHO!
        check.buttonAction("Você clicou em 'RECUAR'!", page)

    if sentido == "COLETAR":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM RECUAR O GUINCHO!
        check.buttonAction("Você clicou em 'COLETAR'!", page)

    if sentido == "SOLTAR":
        # CONECTAR AO SERVIDOR
        # ENVIAR UM COMANDO PARA O COPPELIASIM RECUAR O GUINCHO!
        check.buttonAction("Você clicou em 'SOLTAR'!", page)

# recebimento de dados dos Sensores
def dados(dado):
    if dado == "angulo":
        # CONECTAR AO SERVIDOR
        # retornar o valor do Angulo do guindaste
        return (77)

    if dado == "altura":
        # CONECTAR AO SERVIDOR
        # retornar o valor do Angulo do guindaste
        return (88)

    if dado == "extensao":
        # CONECTAR AO SERVIDOR
        # retornar o valor do Angulo do guindaste
        return (99)
