import PySimpleGUI as sg
import checkAction as check
import connectionServer as cs

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
