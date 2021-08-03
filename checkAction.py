import PySimpleGUI as sg
import controlPage as p1

#aparece uma menssagem certificando que o botão 'x' foi acionado!
def buttonAction(msg, page):
    layout = [
        [sg.Text(' ')],
        [
            sg.Text(msg)
        ],
        [sg.Text(' ')],
        [
            sg.Text('  '), sg.Button('OK')
        ]
    ]

    window = sg.Window('CHECK ACTION MESSAGE', layout, size=(400, 150), element_justification='center')
    button, event = window.read()

    while True:
        if button == 'OK':
            window.close()
            if page == 'p1':
                p1.front()

        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            if page == 'p1':
                p1.front()
    window.exit()