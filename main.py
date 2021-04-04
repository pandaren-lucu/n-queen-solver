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
            board_dict = {}
            board = []
            idx = 1
            for row in range(board_size):
                temp_row = []
                for col in range(board_size):
                    temp_row.append(sg.Button(f'[{row}, {col}]', enable_events=True, key=idx))
                    board_dict[idx] = f'[{row}, {col}]'
                    idx += 1
                board.append(temp_row)
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
            board = []
            idx = 1
            for row in range(board_size):
                temp_row = []
                for col in range(board_size):
                    temp_row.append(sg.Text(f'[{row}, {col}]', key=idx))
                    idx += 1
                board.append(temp_row)
            layout= [
                [sg.Frame('Chess Board', board)],
                [sg.Text(size=(60,1), key='-ERROR-')],
                [sg.Button('Next'), sg.Button('Cancel')]]
            window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
            event, values = window.read()
            clauses = sat.generate_n_queen_clauses(board_size)
            for queen in start_queen:
                clauses.append([queen])
            print('clauses', clauses)
            print('start_queen', start_queen)
            while event != 'Cancel':
                solution = sat.solve_n_queen(board_size, clauses)
                if solution[1] == None:
                    sg.popup('There is no more solution!')
                    if event == 'OK':
                        window.close()
                for queen in solution[2]:
                    if queen > 0:
                        window[queen].update('QQQQ')
                    else:
                        window[-queen].update(board_dict[-queen])
                clauses.append([-queen for queen in solution[2]])
                print('solution', solution)
                print(event, values)
                event, values = window.read()
    except:
        window['-ERROR-'].update('The board size must be an integer')
    print(values)
    event, values = window.read()
window.close()