from typing import Text
import PySimpleGUI as sg
import initialPage as p0
import commands as c0
from commands import Commands
from connectionServer import ConnectionInterface
import numpy as np

import constants as const


class Object(object):
    pass


def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
                    graph_bottom_left=(-radius, -radius),
                    graph_top_right=(radius, radius),
                    pad=(0, 0), key=key)


def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color) 
    
def SetStep(window, stepToSet: str, step: float):
    newStep = np.clip(float(step),float(const.MIN_STEP),float(const.MAX_STEP))
    window[stepToSet].update(round(newStep, 2))
    return newStep

def UpdateVariables(window, connectionLibrary: ConnectionInterface):
    connectionStatus = connectionLibrary.getConnectionStatus()
    craneStatus = connectionLibrary.getCraneStatus()
    magnetStatus = connectionLibrary.getMagnetStatus()

    if connectionStatus and craneStatus:
        window['-ANGULO-'].update(round(connectionLibrary.getCurrentAngleClaw(), 2))
        window['-ALTURA-'].update(round(connectionLibrary.getCurrentHeightHook(), 2))
        window['-EXTENSAO-'].update("xxx")
    else:
        window['-ANGULO-'].update("0")
        window['-ALTURA-'].update("0")
        window['-EXTENSAO-'].update("0")

    if connectionStatus:
        SetLED(window, '_STATUS_', 'green')
    else:
        SetLED(window, '_STATUS_', 'red')

    if craneStatus:
        SetLED(window, '_STATUS_CRANE_', 'green')
    else:
        SetLED(window, '_STATUS_CRANE_', 'red')
        
    if magnetStatus:
        SetLED(window, '_STATUS_MAGNET_', 'green')
    else:
        SetLED(window, '_STATUS_MAGNET_', 'yellow')

    c0.SetCamImage(window, 0, connectionLibrary)

def front():
    layout = [
        [
            sg.Text('SERVER CONNECTION STATUS:  '), LEDIndicator('_STATUS_'),
            sg.Text(' '), sg.Button('CONNECT'), sg.Text('            '),
            sg.Text('CRANE STATUS:  '), LEDIndicator('_STATUS_CRANE_'), sg.Button('INIT/STOP'),
            sg.Text('                                     '), sg.Button('VOLTAR', size=[8, 1]), sg.Text(' '), sg.Button('SAIR', size=[8, 1])
        ],
        [
            sg.Frame(layout=[
                [
                    sg.Text('ÂNGULO DO GUINDASTE', size=(
                        45, 1), justification='center'),
                    sg.Text('ALTURA DO GUINCHO', size=(
                        45, 1), justification='center'),
                    sg.Text('EXTENSÃO DO BRAÇO', size=(
                        45, 1), justification='center')
                ],
                [
                    sg.Image(r"Assets/img_angulo.png"),
                    sg.Image(r"Assets/img_altura.png"),
                    sg.Image(r"Assets/img_extensao.png")
                ],
                [
                    sg.Frame(layout=[[sg.Text(size=(17, 1), justification='center', font=(
                        "Helvetica", 25), key='-ANGULO-')]], title=''),
                    sg.Frame(layout=[[sg.Text(size=(17, 1), justification='center', font=(
                        "Helvetica", 25), key='-ALTURA-')]], title=''),
                    sg.Frame(layout=[[sg.Text(size=(17, 1), justification='center', font=(
                        "Helvetica", 25), key='-EXTENSAO-')]], title='')
                ]
            ], title='Posições')
        ],
        [
            sg.Frame(layout=[
                [sg.Text(' ')],
                [
                    sg.Text(' '), sg.Button('SUBIR', size=[15, 1]), sg.Text('  '), 
                    sg.Button('-', size=[3, 1], key='s-altura'), sg.Text(str(float(const.MIN_STEP)),size=[3, 1],key='stepAlturaText'), sg.Button('+', size=[3, 1], key='s+altura'), 
                    sg.Text('  '), sg.Button('DESCER', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('ESQUERDA', size=[15, 1]), sg.Text('  '), 
                    sg.Button('-', size=[3, 1], key='s-angulo'), sg.Text(str(float(const.MIN_STEP)),size=[3, 1], key='stepAnguloText'), sg.Button('+', size=[3, 1], key='s+angulo'), 
                    sg.Text('  '), sg.Button('DIREITA', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('AVANÇAR', size=[15, 1]), sg.Text('  '), 
                    sg.Button('-', size=[3, 1], key='s-extensao'), sg.Text(str(float(const.MIN_STEP)),size=[3, 1], key='stepExtensaoText'), sg.Button('+', size=[3, 1], key='s+extensao'), 
                    sg.Text('  '), sg.Button('RECUAR', size=[15, 1])
                ],
                [sg.Text(' ')],
                [
                    sg.Text(' '), sg.Frame(layout=[
                        [
                            sg.Button('COLETAR', size=[15, 1]), sg.Text('    '), sg.Frame(
                                layout=[[sg.Text(' '), LEDIndicator('_STATUS_MAGNET_'), sg.Text(' ')]], title=''), sg.Text('   '), sg.Button('SOLTAR', size=[15, 1])
                        ]
                    ], title='')
                ],
                [sg.Text(' ')],
            ], title='Comandos'),
            sg.Text('                     '), sg.Frame(layout=[
                [sg.Image(r"Assets/img_guindaste04.png", key='cam1', size=(600, 600))]], title='Video-Simulação')
        ],
    ]

    window = sg.Window('GRUPO C - GUINDASTE VIRTUAL', layout, size=(1050, 650))
    SetLED(window, '_STATUS_', 'red')

    connectionLibrary = ConnectionInterface()
    commandsLibrary = Commands()
    
    stepAltura = const.MIN_STEP
    stepAngulo = const.MIN_STEP
    stepExtensao = const.MIN_STEP
    
    count = 0

    while True:
        button, event = window.read(timeout=const.FREQUENCY_UPDATE_DATA)
        count += 1
        UpdateVariables(window, connectionLibrary)

        if button == 'SAIR':
            statusCrane = connectionLibrary.getCraneStatus()
            if statusCrane:
                connectionLibrary.commandCraneOnOff()
            break

        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            statusCrane = connectionLibrary.getCraneStatus()
            if statusCrane:
                connectionLibrary.commandCraneOnOff()
            break

        elif button == 'SUBIR':
            commandsLibrary.SUBIR(window, stepAltura, connectionLibrary)
            UpdateVariables(window, connectionLibrary)

        elif button == 'DESCER':
            commandsLibrary.DESCER(window, stepAltura, connectionLibrary)
            UpdateVariables(window, connectionLibrary)
            
        elif button == 's-altura':
            stepAltura = SetStep(window, 'stepAlturaText', stepAltura - 0.5)
            
        elif button == 's+altura':
            stepAltura = SetStep(window, 'stepAlturaText', stepAltura + 0.5)

        elif button == 'ESQUERDA':
            commandsLibrary.ESQUERDA(window, stepAngulo, connectionLibrary)
            UpdateVariables(window, connectionLibrary)

        elif button == 'DIREITA':
            commandsLibrary.DIREITA(window, stepAngulo, connectionLibrary)
            UpdateVariables(window, connectionLibrary)
            
        elif button == 's-angulo':
            stepAngulo = SetStep(window, 'stepAnguloText', stepAngulo - 1)
            
        elif button == 's+angulo':
            stepAngulo = SetStep(window, 'stepAnguloText', stepAngulo + 1)

        elif button == 'AVANÇAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'AVANÇAR'
            c0.comandos('AVANÇAR', 'p1')

        elif button == 'RECUAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'RECUAR'
            c0.comandos('RECUAR', 'p1')
            
        elif button == 's-extensao':
            stepExtensao = SetStep(window, 'stepExtensaoText', stepExtensao - 1)
            
        elif button == 's+extensao':
            stepExtensao = SetStep(window, 'stepExtensaoText', stepExtensao + 1)

        elif button == 'COLETAR':
            statusMagnet = connectionLibrary.getMagnetStatus()
            if not statusMagnet:
                commandsLibrary.MAGNET(window, connectionLibrary)
            UpdateVariables(window, connectionLibrary)

        elif button == 'SOLTAR':
            statusMagnet = connectionLibrary.getMagnetStatus()
            if statusMagnet:
                commandsLibrary.MAGNET(window, connectionLibrary)
            UpdateVariables(window, connectionLibrary)

        elif button == 'CONNECT':
            SetLED(window, '_STATUS_', 'red')
            statusConnection = connectionLibrary.getConnectionStatus()
            if not statusConnection:
                _, status = connectionLibrary.init_connection(
                    const.IP_SERVER, 19997)
                if status:
                    SetLED(window, '_STATUS_', 'green')

        elif button == 'INIT/STOP':
            connectionLibrary.commandCraneOnOff()

        elif button == 'VOLTAR':
            window.close()
            p0.front()
            break
        
    window.close()
