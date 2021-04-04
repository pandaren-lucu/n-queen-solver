import sat
import PySimpleGUI as sg

sg.theme('TanBlue')

layout = [  [sg.Text('Please input the board size (8-16)')],
            [sg.Text('Board size:'), sg.InputText(key='-SIZE-')],
            [sg.Text(size=(60,1), key='-ERROR-')],
            [sg.Button('Start'), sg.Button('Cancel')] ]

window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
event, values = window.read()
while event != sg.WIN_CLOSED and event != 'Cancel':
    try:
        board_size = int(values['-SIZE-'])
        if board_size < 8 or board_size > 16:
            window['-ERROR-'].update('The board size must be between 8-16')
        else:
            window.close()
            board = [[sg.Button(f'[{row}, {col}]', enable_events=True) for col in range(board_size)] for row in range(board_size)]
            layout= [
                [sg.Frame('Chess Board', board)],
                [sg.Text(size=(60,1), key='-ERROR-')],
                [sg.Button('Solve'), sg.Button('Cancel')]]
            window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
            event, values = window.read()
            start_queen = []
            while event != 'Solve':
                start_queen.append(event)
                window[event].update(disabled=True)
                event, values = window.read()
            window.close()
            board = [[sg.Text(f'[{row}, {col}]', key=f'[{row}, {col}]') for col in range(board_size)] for row in range(board_size)]
            layout= [
                [sg.Frame('Chess Board', board)],
                [sg.Text(size=(60,1), key='-ERROR-')],
                [sg.Button('Next'), sg.Button('Cancel')]]
            window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
            event, values = window.read()
            while event != 'Cancel':
                for queen in start_queen:
                    window[queen].update('QQQQ')
                print(start_queen)
                event, values = window.read()
    except:
        window['-ERROR-'].update('The board size must be an integer')
    print(values)
    event, values = window.read()
window.close()