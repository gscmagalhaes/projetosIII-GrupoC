"""
PROJETO DE LABORATÓRIO EM ENGENHARIA DE SISTEMAS III
Essa Gui é uma ferramenta utilizada para controlar a simulação de um guindaste remotamente.
A simulação do Guindaste será realizada através do software CoppeliaSim

GRUPO C

Alunos:
    - Daniel Souza
    - Gabriel Magalhães
    - Letícia Machado
    - Maria Fernanda Fávaro
    - Thiago de Mello

DOCUMENTATION
PySimpleGUI
https://pysimplegui.readthedocs.io/en/latest/
https://pypi.org/project/PySimpleGUI/

page updates
https://pysimplegui.readthedocs.io/en/latest/#persistent-window-example-running-timer-that-updates

LED indications
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_LED_Indicators.py

Layout
https://pysimplegui.readthedocs.io/en/latest/cookbook/

"""

import PySimpleGUI as sg
import initialPage as p0

#tema geral do aplicativo
sg.theme('DarkGrey6')

#requisição da pagina inicial
p0.front()
