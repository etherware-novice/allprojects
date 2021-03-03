board = [[0, 0, 0],
[0, 0, 0],
[0, 0, 0]]

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cell.append([x, y])
    return cells
    pass

def valid_move(x, y):
    return [x, y] in empty_cells(board)

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return true
    return false

def render(state, c_choice, h_choice):
    for row in state:
        print('\n----------------')
        for cell in row:
            if cell == COMP:
                print('|', c_choice, '|', end='')
            elif cell == HUMAN:
                print('|', h_choice, '|', end='')
            else:
                print('|', ' ', '|', end='')
        print('\n----------------')

def evaluate(state):
    if wins(state, COMP):
        score = 1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)


def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score # max value
        else:
            if score[2] < best[2]:
                best = score # min value
    return best

def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print('Computers turn [{}]'.format(c_choice))
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    sleep(1)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print('Human turn [{}]'.format(h_choice))
    render(board, c_choice, h_choice)

    while (move < 1 or move > 9):
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            try_move = set_move(coord[0], coord[1], HUMAN)

            if not try_move:
                print('Invalid move.')
                move = -1
        except KeyboardInterrupt:
            print('Goodbye!')
            exit()
        except:
            print('Invalid move.')

def main():
    clean()
    h_choice = ''
    c_choice = ''
    first = ''

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except KeyboardInterrupt:
            print('Goodbye!')
            exit()
        except:
            print('Invalid choice.')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start? [y/n]: ').upper()
        except KeyboardInterrupt:
            print('Goodbye!')
            exit()
        except:
            print('Invalid choice.')

    # Main game loop
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print('Human turn [{}]'.format(h_choice))
        render(board, c_choice, h_choice)
        print('You win!')
    elif wins(board, COMP):
        clean()
        print('Computer turn [{}]'.format(c_choice))
        render(board, c_choice, h_choice)
        print('Computer wins!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('It\'s a tie!')

    exit()
