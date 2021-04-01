import sat
import PySimpleGUI as sg

sg.theme('TanBlue')

layout = [  [sg.Text('Please input the board size (8-16)')],
            [sg.Text('Board size:'), sg.InputText(key='-BOARD-')],
            [sg.Text(size=(60,1), key='-ERROR-')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)

while True:
    event, values = window.read()
    if event == 'Ok':
        try:
            board_size = int(values['-BOARD-'])
            if board_size < 8 or board_size > 16:
                window['-ERROR-'].update('The board size must be between 8-16')
            else:
                window['-ERROR-'].update('YEY')
        except:
            window['-ERROR-'].update('The board size must be an integer')
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print('You entered ', values['-BOARD-'])

window.close()