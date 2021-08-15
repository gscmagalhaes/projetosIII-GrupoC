import PySimpleGUI as sg
import controlPage as p1

def front():
    layout = [
        [sg.Text(' ')],
        [sg.Text('SIMULAÇÃO DO GUINDASTE')],
        [sg.Text(' ')],
        [sg.Button('INICIAR'), sg.Button('SAIR')]
    ]

    window = sg.Window('GRUPO C - GUINDASTE VIRTUAL', layout, size=(400, 150), element_justification='center')
    
    while True:
        button, event = window.read()

        if button == 'INICIAR':
            window.close()
            p1.front()
            break
        
        else:
            window.close()
            break