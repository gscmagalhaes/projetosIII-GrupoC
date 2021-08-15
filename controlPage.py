import PySimpleGUI as sg
import initialPage as p0
import commands as c0
from commands import Commands
import connectionServer as cs
from connectionServer import ConnectionInterface

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


def UpdateVariables(window, connectionLibrary: ConnectionInterface):
    connectionStatus = connectionLibrary.getConnectionStatus()
    craneStatus = connectionLibrary.getCraneStatus()

    if connectionStatus and craneStatus:
        window['-ANGULO-'].update("xxx")
        window['-ALTURA-'].update(round(connectionLibrary.getCurrentHeightHook(), 2))
        window['-EXTENSAO-'].update("xxx")
    else:
        window['-ANGULO-'].update("0")
        window['-ALTURA-'].update("0")
        window['-EXTENSAO-'].update("0")

    if connectionStatus :
        SetLED(window, '_STATUS_', 'green')
    else:
        SetLED(window, '_STATUS_', 'red')

    if craneStatus:
        SetLED(window, '_STATUS_CRANE_', 'green')
    else:
        SetLED(window, '_STATUS_CRANE_', 'red')
    
    SetLED(window, '_STATUS_MAGNET_', 'yellow')


def front():
    layout = [
        [
            sg.Text('SERVER CONNECTION STATUS:  '), LEDIndicator('_STATUS_'),
            sg.Text(' '), sg.Button('CONNECT'), sg.Text('            '),
            sg.Text('CRANE STATUS:  '), LEDIndicator('_STATUS_CRANE_'), sg.Button('INIT/STOP')
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
                    sg.Text(' '), sg.Button('SUBIR', size=[15, 1]), sg.Text('  '), sg.Button('DESCER', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('ESQUERDA', size=[15, 1]), sg.Text('  '), sg.Button('DIREITA', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('AVANÇAR', size=[15, 1]), sg.Text('  '), sg.Button('RECUAR', size=[15, 1])
                ],
                [sg.Text(' ')],
                [
                    sg.Frame(layout=[
                        [
                            sg.Button('COLETAR', size=[15, 1]), sg.Frame(
                                layout=[[LEDIndicator('_STATUS_MAGNET_')]], title=''), sg.Button('SOLTAR', size=[15, 1])
                        ]
                    ], title='')
                ],
                [sg.Text(' ')],
                [
                    sg.Text('             '), sg.Button('VOLTAR', size=[8, 1]), sg.Text(
                        '  '), sg.Button('SAIR', size=[8, 1])
                ],
                [sg.Text(' ')],
                [sg.Text(' ')]
            ], title='Comandos'), sg.Text('                     '), sg.Frame(layout=[[sg.Image(r"Assets/img_guindaste04.png")]], title='Video-Simulação')
        ]
    ]

    window = sg.Window('GRUPO C - GUINDASTE VIRTUAL', layout, size=(1050, 650))
    SetLED(window, '_STATUS_', 'red')
    
    connectionLibrary = ConnectionInterface()
    commandsLibrary = Commands()

    while True:       
        button, event = window.read(timeout=const.FREQUENCY_UPDATE_DATA) 
        
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
            commandsLibrary.SUBIR(connectionLibrary)

        elif button == 'DESCER':
            commandsLibrary.DESCER(connectionLibrary)

        elif button == 'ESQUERDA':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'ESQUERDA'
            c0.comandos('ESQUERDA', 'p1')

        elif button == 'DIREITA':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'DIREITA'
            c0.comandos('DIREITA', 'p1')

        elif button == 'AVANÇAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'AVANÇAR'
            c0.comandos('AVANÇAR', 'p1')

        elif button == 'RECUAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'RECUAR'
            c0.comandos('RECUAR', 'p1')

        elif button == 'COLETAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'RECUAR'
            c0.comandos('COLETAR', 'p1')

        elif button == 'SOLTAR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'RECUAR'
            c0.comandos('SOLTAR', 'p1')
            
        elif button == 'CONNECT':
            SetLED(window, '_STATUS_', 'red') 
            statusConnection = connectionLibrary.getConnectionStatus()
            if not statusConnection:
                _, status = connectionLibrary.init_connection('127.0.0.1' , 19997)
                if status:
                    SetLED(window, '_STATUS_', 'green')  
                    
        elif button == 'INIT/STOP':
            connectionLibrary.commandCraneOnOff()
                
        elif button == 'VOLTAR':
            window.close()
            p0.front()
            break

    window.close()       