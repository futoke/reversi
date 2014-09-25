import os
import sys
import time
import random

BOARD_SIZE = 8
BLACK_CHIP = '■'
WHITE_CHIP = '¤'


def draw_board(board):
    """Данная функция выводит на экран игровое поле с текущем расположением
    фишек.

    Возвращаемое значение: None.
    """

    HLINE = '   ├───┼───┼───┼───┼───┼───┼───┼───┤'

    os.system('cls')

    print('     а   б   в   г   д   е   ж   з') 
    print('   ┌───┬───┬───┬───┬───┬───┬───┬───┐')

    for y in range(BOARD_SIZE):
        print('', y + 1 , end=' ')

        for x in range(BOARD_SIZE):
            print('│ {}'.format(board[x][y]), end=' ')
        print('│')

        if y != BOARD_SIZE - 1:
            print(HLINE)

    print('   └───┴───┴───┴───┴───┴───┴───┴───┘')


def reset_board(board):
    """Данная функция осуществляет начальное расположение фишек.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.

    Возвращаемое значение: None
    """

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            board[x][y] = ' '

    board[3][3] = BLACK_CHIP
    board[3][4] = WHITE_CHIP
    board[4][3] = WHITE_CHIP
    board[4][4] = BLACK_CHIP


def getNewBoard():
    """Данная функция создает пустое игровое поле.

    Возвращаемое значение: двумерный список "клеток" игрового поля.
    """
    
    board = []
    for i in range(BOARD_SIZE):
        board.append([' '] * BOARD_SIZE)

    return board


def is_valid_move(board, tile, xstart, ystart):
    """Данная функция проверяет правильность сделанного хода.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        tile -- фишка, которой ходит игрок.
        xstart -- координата текущего хода по Х.
        ystart -- координата текущего хода по Y.

    Возвращаемое значение:
        False -- в случае, если игрок пытается поставить фишку на занятую клетку
            или за пределы игрового поля, либо делает ход, который не позволит
            ему перевернуть фишки противника.
        
        ИЛИ

        Список координат фишек противника, которые игрок может перевернуть этим 
        ходом.
    """

    if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
        return False

    board[xstart][ystart] = tile

    if tile == BLACK_CHIP:
        other_tile = WHITE_CHIP
    else:
        other_tile = BLACK_CHIP

    tiles_to_flip = []
    for xdirection, ydirection in [[0, 1],  [1, 1],   [1, 0],  [1, -1],
                                   [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection

        if is_on_board(x, y) and board[x][y] == other_tile:
            x += xdirection
            y += ydirection

            if not is_on_board(x, y):
                continue

            while board[x][y] == other_tile:
                x += xdirection
                y += ydirection

                if not is_on_board(x, y):
                    break

            if not is_on_board(x, y):
                continue

            if board[x][y] == tile:

                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tiles_to_flip.append([x, y])

    board[xstart][ystart] = ' ' # Очищаем позицию проверяемого хода

    if len(tiles_to_flip) == 0: # Если не удалось перевернуть ни одной фишки
        return False            # противника -- возвращаем False
        
    return tiles_to_flip


def is_on_board(x, y):
    """Данная функция проверяет принадлежность заданной клетки игровому полю.

    Аргументы:
        x -- координата х проверяемой клетки.
        y -- координата y проверяемой клетки.

    Возвращаемое значение:
        True -- если клетка принадлежит игровому полю
        False -- в противном случае.
    """
    return (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE)


def get_board_with_valid_moves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    """Данная функция создает новое временное игровое поле, на котором 
    символом '.' помечены клетки куда можно сделать ход.

    Аргументы:
        board -- игровое поле.
        tile -- фишка, которой ходит игрок.

    Возвращаемое значение: новое игровое поле с помеченными клетками в виде
        списка.
    """

    dupe_board = get_board_copy(board)

    for x, y in get_valid_moves(dupe_board, tile):
        dupe_board[x][y] = '.'
    return dupe_board


def get_valid_moves(board, tile):
    """Данная функция возвращает список возможных допустимых ходов для текущего
    игрока на текущем ходе.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        tile -- фишка, которой ходит игрок.

    Возвращаемое значение: список коодинат клеток.
    """

    valid_moves = []

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, tile, x, y):
                valid_moves.append([x, y])
    return valid_moves


def get_score_of_board(board):
    """Данная функция рассчитывает текущее распределение очков.

    Аргументы:
         board -- текущее расположение фишек на игровом поле.

    Возвращаемое значение: словарь с количеством очков у обоих игроков.
    """


    black_score, white_score = 0, 0

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == BLACK_CHIP:
                black_score += 1
            if board[x][y] == WHITE_CHIP:
                white_score += 1
    return {BLACK_CHIP:black_score, WHITE_CHIP:white_score}


def enter_player_tile():
    """Данная функция предлагает пользователю выбрать фишкой какого цвета одной
    будет играть.

    Возвращаемое значение: кортеж из двух элементов, в котором на первом месте
    указана фишка пользователя, а на втором -- компьютера.
    """
    
    tile = ''
    while tile not in ('Б', 'Ч'):
        tile = input('Вы хотите играть [Б]елыми или [Ч]ёрными? ').upper()

    if tile.startswith('Ч'):
        return (BLACK_CHIP, WHITE_CHIP)
    else:
        return (WHITE_CHIP, BLACK_CHIP)


def who_goes_first():
    """Данная функция выбирает кто делает первый ход.

    Возвращаемое значение: один из элементов кортежа ('Компьютер','Игрок'),
    выбраный произвольным образом.
    """

    return random.choice(('Компьютер', 'Игрок'))


def play_again():
    """Данная функция проверяет хочет ли пользователь сыграть еще раз.

    Возвращаемое значение:
        True -- если пользователь хочет сыграть еще раз.
        False --  в противном случае.
    """

    return input('Хотите сыграть еще раз (да или нет):').lower().startswith('д')


def make_move(board, tile, xstart, ystart):
    """Данная функция ставит фишку игрока на заданную клетку и переворачивает
    фишки противника.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        tile -- фишка, которой ходит игрок.
        xstart -- координата текущего хода по Х.
        ystart -- координата текущего хода по Y.

    Возвращаемое значение:
        True -- если ход является допустимым.
        False -- в противном случае.
    """
    
    tiles_to_flip = is_valid_move(board, tile, xstart, ystart)

    if not tiles_to_flip:
        return False

    board[xstart][ystart] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True


def get_board_copy(board):
    """Данная функция создает копию текущего игровго поля.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.

    Возвращаемое значение: копия игрового поля в виде списка.
    """
    
    dupe_board = getNewBoard()

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            dupe_board[x][y] = board[x][y]

    return dupe_board


def is_on_corner(x, y):
    """Данная функция проверяет является ли клетка угловой.

    Аргументы:
        x -- координата х проверяемой клетки.
        y -- координата y проверяемой клетки.

    Возвращаемое значение:
        True -- если клетка является угловой.
        False -- в противном случае.
    """
    # return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)
    return (x, y) in ((0, 0), (BOARD_SIZE - 1, 0),
                    (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, BOARD_SIZE - 1))


def get_player_move(board, tile):
    """Данная функция предлагает пользователю сделать ход и обрабатывает 
    полученные данные.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        tile -- фишка, которой ходит игрок.

    Возвращаемое значение:
        Список коодинат в виде [x, y] -- если полъзователь сделал ход.
        Строка 'выход' -- если пользователь хочет выйти и ввел 'У'.
        Строка 'подсказки' -- если пользователь хочет переключить отображение
            подсказок и ввел 'П'.
        """
    DIGITS = '12345678'
    CHARS = 'абвгдежз'

    MSG_NOT_VALID_TURN = 'Вы сделали неверный ход.'
    while True:
        move = input('Ваш ход (У - выйти, П - вкл./выкл. подсказки): ').lower()
        if move.startswith('у'):
            return 'выход'
        if move.startswith('п'):
            return 'подсказки'

        if len(move) == 2 and move[0] in CHARS and move[1] in DIGITS:
            x = CHARS.index(move[0])
            y = DIGITS.index(move[1])
            if not is_valid_move(board, tile, x, y):
                print(MSG_NOT_VALID_TURN)
                continue
            else:
                break
        else:
            print(MSG_NOT_VALID_TURN)

    return [x, y]


def get_computer_move(board, tile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    """Данная функция делает ход за компьютер.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        tile -- фишка, которой ходит компьютер.

    Возвращаемое значение:
        Список коодинат в виде [x, y].
    """
    possible_moves = get_valid_moves(board, tile)

    random.shuffle(possible_moves)

    # Если есть возможность, всегда ставить фишку в угол игрового поля.
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]

    # Пройти по всему списку ходов и выбрать наиболее результативный.
    best_score = -1
    for x, y in possible_moves:
        dupe_board = get_board_copy(board)
        make_move(dupe_board, tile, x, y)
        score = get_score_of_board(dupe_board)[tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def show_points(board, player_tile, computer_tile):
    """Данная функция выводит на экран текущее распределение очков.

    Аргументы:
        board -- текущее расположение фишек на игровом поле.
        player_tile -- фишка, которой ходит игрок.
        computer_tile -- фишка, которой ходит компьютер.

    Возвращаемое значение: None
    """

    tiles = {BLACK_CHIP:'(чёрные)', WHITE_CHIP:'(белые)'}
    scores = get_score_of_board(board)
    print('У вас {} -- {}, у компьютера {} -- {}.'.format(tiles[player_tile],
                                                          scores[player_tile],
                                                          tiles[computer_tile],
                                                          scores[computer_tile]))

def main():
    """Основной цикл программы
    """

    show_hints = False

    os.system('cls')
    print('Добро пожаловать в игру Реверси!')

    while True:

        main_board = getNewBoard()
        reset_board(main_board)
        player_tile, computer_tile = enter_player_tile()
        
        turn = who_goes_first()
        print(turn, 'ходит первым.')
        time.sleep(1)
        os.system('cls')

        while True:
            if turn == 'Игрок':
                if show_hints:
                    valid_moves_board = get_board_with_valid_moves(main_board,
                                                                   player_tile)
                    draw_board(valid_moves_board)
                else:
                    draw_board(main_board)

                show_points(main_board, player_tile, computer_tile)
                move = get_player_move(main_board, player_tile)

                if move == 'выход':
                    print('Спасибо за игру!')
                    sys.exit()
                elif move == 'подсказки':
                    show_hints = not show_hints
                    continue
                else:
                    make_move(main_board, player_tile, move[0], move[1])

                if get_valid_moves(main_board, computer_tile) == []:
                    break
                else:
                    turn = 'Компьютер'

            else:
                # Computer's turn.
                draw_board(main_board)
                show_points(main_board, player_tile, computer_tile)
                # input('Press Enter to see the computer\'s move.')
                x, y = get_computer_move(main_board, computer_tile)
                make_move(main_board, computer_tile, x, y)

                if get_valid_moves(main_board, player_tile) == []:
                    break
                else:
                    turn = 'Игрок'

        # Display the final score.
        draw_board(main_board)
        scores = get_score_of_board(main_board)
        print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
        if scores[player_tile] > scores[computer_tile]:
            print('You beat the computer by %s points! Congratulations!' % (scores[player_tile] - scores[computer_tile]))
        elif scores[player_tile] < scores[computer_tile]:
            print('You lost. The computer beat you by %s points.' % (scores[computer_tile] - scores[player_tile]))
        else:
            print('The game was a tie!')

        if not play_again():
            break


if __name__ == '__main__':
    main()
