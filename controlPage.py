import PySimpleGUI as sg
import initialPage as p0
import comands as c0
import connectionServer as cs

import constants as const

def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
                    graph_bottom_left=(-radius, -radius),
                    graph_top_right=(radius, radius),
                    pad=(0, 0), key=key)


def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)


def UpdateVariables(window):
    print('Update Variables Data')

    window['-ANGULO-'].update(c0.dados('angulo'))
    window['-ALTURA-'].update(c0.dados('altura'))
    window['-EXTENSAO-'].update(c0.dados('extensao'))

    # LED de indicação para teste de conexão
    statusLED = cs.connectionStatus()
    if statusLED == 'off':
        SetLED(window, '_STATUS_', 'red')
    elif statusLED == 'on':
        SetLED(window, '_STATUS_', 'green')
    if statusLED == 'wait':
        SetLED(window, '_STATUS_', 'yellow')

    # LED de indicação para teste de conexão
    getLED = cs.getObjectStatus()
    if getLED == 'free':
        SetLED(window, '_GET_', 'green')
    elif getLED == 'hold':
        SetLED(window, '_GET_', 'blue')
    if getLED == 'tring':
        SetLED(window, '_GET_', 'yellow')


def front():
    layout = [
        [
            sg.Text('SERVER CONNECTION STATUS:  '), LEDIndicator('_STATUS_')
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
                    sg.Button('Atualizar')
                ],
                [sg.Text(' ')],
                [
                    sg.Text(' '), sg.Button('SUBIR', size=[15, 1]), sg.Text(
                        '  '), sg.Button('DESCER', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('ESQUERDA', size=[15, 1]), sg.Text(
                        '  '), sg.Button('DIREITA', size=[15, 1])
                ],
                [
                    sg.Text(' '), sg.Button('AVANÇAR', size=[15, 1]), sg.Text(
                        '  '), sg.Button('RECUAR', size=[15, 1])
                ],
                [sg.Text(' ')],
                [
                    sg.Frame(layout=[
                        [
                            sg.Button('COLETAR', size=[15, 1]), sg.Frame(
                                layout=[[LEDIndicator('_GET_')]], title=''), sg.Button('SOLTAR', size=[15, 1])
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

    while True:
        button, event = window.read(timeout=const.FREQUENCY_UPDATE_DATA) 

        UpdateVariables(window)

        if button == 'SAIR':
            break

        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        elif button == 'SUBIR':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'SUBIR'
            c0.comandos('SUBIR', 'p1')

        elif button == 'DESCER':
            window.close()  # EXCLUIR LINHA APÓS IMPLEMENTAÇÃO DA FUNÇÃO: 'DESCER'
            c0.comandos('DESCER', 'p1')

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

        elif button == 'VOLTAR':
            window.close()
            p0.front()
            break

    window.exit()
