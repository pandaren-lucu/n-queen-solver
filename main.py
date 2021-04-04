import sat
import PySimpleGUI as sg

sg.theme('Black')

layout = [  [sg.Text('Please input the board size (8-15)')],
            [sg.Text('Board size:'), sg.InputText(key='-SIZE-')],
            [sg.Text(size=(40,1), key='-ERROR-')],
            [sg.Button('Start', size=(10,2))] ]

window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
event, values = window.read()

while event != sg.WIN_CLOSED:
    try:
        board_size = int(values['-SIZE-'])

        if board_size < 8 or board_size > 15:
            window['-ERROR-'].update('The board size must be between 8-15')           
        else:
            window.close()
            board_dict = {}
            board = []
            idx = 1

            for row in range(board_size):
                temp_row = []

                for col in range(board_size):
                    if (col + row) % 2 == 0:
                        temp_row.append(sg.Button(f'[{row+1}, {col+1}]', button_color=('white', 'black'), enable_events=True, key=idx, size=(6,3)))
                    else:
                        temp_row.append(sg.Button(f'[{row+1}, {col+1}]', button_color=('black', 'white'), enable_events=True, key=idx, size=(6,3)))
                    board_dict[idx] = [f'[{row+1}, {col+1}]', (col + row) % 2]
                    idx += 1
                board.append(temp_row)

            layout= [
                [sg.Frame('Chess Board', board)],
                [sg.Text(size=(40,1), key='-ERROR-')],
                [sg.Button('Solve', size=(10,2))]]

            window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
            event, values = window.read()
            start_queen = []

            while event != 'Solve':
                start_queen.append(event)
                window[event].update('Queen', button_color=('white', 'yellow'), disabled=True)
                event, values = window.read()

            window.close()
            board = []
            idx = 1

            for row in range(board_size):
                temp_row = []
                for col in range(board_size):
                    if (col + row) % 2 == 0:
                        temp_row.append(sg.Button(f'[{row+1}, {col+1}]', button_color=('white', 'black'), enable_events=True, key=idx, size=(6,3), disabled=True))
                    else:
                        temp_row.append(sg.Button(f'[{row+1}, {col+1}]', button_color=('black', 'white'), enable_events=True, key=idx, size=(6,3), disabled=True))
                    idx += 1
                board.append(temp_row)

            layout= [
                [sg.Frame('Chess Board', board)],
                [sg.Text(size=(40,1), key='-ERROR-')],
                [sg.Button('Start MiniSat', size=(10,2), key='-NEXT-')]]

            window = sg.Window('N-Queen Solver by Pandaren Lucu', layout)
            event, values = window.read()
            window['-NEXT-'].update('Next solution')
            clauses = sat.generate_n_queen_clauses(board_size)

            for queen in start_queen:
                clauses.append([queen])

            while event != sg.WIN_CLOSED:
                solution = sat.solve_n_queen(board_size, clauses)

                if solution[1] == None:
                    sg.popup('There is no more solution!')
                    window.close()

                for queen in solution[2]:
                    if queen > 0:
                        window[queen].update('Queen', button_color=('white', 'yellow'))
                    elif board_dict[-queen][1] == 0:
                        window[-queen].update(board_dict[-queen][0], button_color=('white', 'black'))
                    else:
                        window[-queen].update(board_dict[-queen][0], button_color=('black', 'white'))
                        
                clauses.append([-queen for queen in solution[2]])
                event, values = window.read()

    except:
        window['-ERROR-'].update('The board size must be an integer')

    event, values = window.read()

window.close()