import pygame


'''Пояснение:
На данный момент есть функции, рисующие первичное поле и иконки кораблей
Пока что только при нажатии на однопалубный корабль можно поставить 4 однопалубных
При нажатии на уже поставленный корабль, тот исчезает (т.е. убирается с поля)
Вокруг кораблей подсвечивается красная зона - туда ставить нельзя
После расстановки всех кораблей меняется цвет кнопочки внизу
При нажатии на кнопку рисуются два поля: компьютера (справа) и игрока с кораблями (слева)

Что ещё нужно сделать:
0.0. Функция удаления однопалубных барахлит - если поставить рядом четыре,
    а затем один удалить, красная окантовка частично пропадёт; надо исправить
0.1. На вторичном поле между зонами игрока и компьютера поставить стрелочку (кто ходит)
1. Насписать функции для расстановки 2-, 3- и 4-хпалубных кораблей вместе с красной подсветкой
2. Написать функции для поворота больших кораблей (например, по нажатию кнопки какой-нибудь)
3. Написать функции для рандомной расстановки кораблей компьютера
4. Написать функции игры (поочерёдные удары)
'''

class Board:
    def __init__(self):  # инициализация
        self.board = [[0] * 10 for _ in range(10)]
        self.numberofcells = 0
        self.mouse_ship = False
        self.running = False
        self.num1, self.num2, self.num3, self.num4 = '4', '3', '2', '1'
        self.stage2 = False

    def render1(self, s):  # рисует кораблики (справа) и поле, отвечает за кол-во корабликов
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(s, ('white'), (10 + i * 40, 10 + j * 40, 40, 40), width=1)
        if int(self.num1) > 0:
            pygame.draw.rect(s, (0, 150, 150), (430, 280, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num1, True, (100, 255, 100))
            screen.blit(text, (480, 285))
        if int(self.num2) > 0:
            for i in range(2):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 220, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num2, True, (100, 255, 100))
            screen.blit(text, (520, 225))
        if int(self.num3) > 0:
            for i in range(3):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 160, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num3, True, (100, 255, 100))
            screen.blit(text, (560, 165))
        if int(self.num4) > 0:
            for i in range(4):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 100, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num4, True, (100, 255, 100))
            screen.blit(text, (600, 105))
        if int(self.num1) + int(self.num2) + int(self.num3) + int(self.num4) != 0:
            pygame.draw.rect(s, (0, 150, 0), (460, 350, 150, 40))
        else:
            pygame.draw.rect(s, (0, 255, 0), (460, 350, 150, 40))

    def render2(self, screen):  # рисует два поля
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(screen, ('white'), (10 + i * 40, 10 + j * 40, 40, 40), width=1)
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(screen, ('white'), (430 + i * 40, 10 + j * 40, 40, 40), width=1)

    def proof1(self, sc, i, j):  # проверяет единичку на возможность постановки
        i2, i1, j2, j1 = i, i, j, j
        if i > 0:
            i2 = i - 1
        if i < 9:
            i1 = i + 1
        if j > 0:
            j2 = j - 1
        if j < 9:
            j1 = i + 1
        if sc.get_at((i * 40 + 15, j * 40 + 15))[:3] == (0, 0, 0):
            if sc.get_at((i * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                if sc.get_at((i1 * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                    if sc.get_at((i1 * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                        if sc.get_at((i1 * 40 + 15, j * 40 + 15))[:3] != (0, 100, 100):
                            if sc.get_at((i2 * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                                if sc.get_at((i2 * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                                    if sc.get_at((i2 * 40 + 15, j * 40 + 15))[:3] != (0, 100, 100):
                                        if sc.get_at((i * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                                            return True

    def ships(self, screen):  # вырисовывает корабли и красные зоны на каждом flip
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == 2:
                    if not self.stage2:
                        if i > 0 and j > 0:
                            self.board[i - 1][j - 1] = 1
                        if j < 9 and i < 9:
                            self.board[i + 1][j + 1] = 1
                        if i > 0:
                            self.board[i - 1][j] = 1
                        if i < 9:
                            self.board[i + 1][j] = 1
                        if j < 9:
                            self.board[i][j + 1] = 1
                        if j > 0:
                            self.board[i][j - 1] = 1
                        if i < 9 and j > 0:
                            self.board[i + 1][j - 1] = 1
                        if i > 0 and j < 9:
                            self.board[i - 1][j + 1] = 1
                    pygame.draw.rect(screen, (0, 100, 100), (i * 40 + 10, j * 40 + 10, 40, 40))
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), (i * 40 + 10, j * 40 + 10, 40, 40))

    def set_single(self):  # ставит единичку
        for i in range(10):
            if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                for j in range(10):
                    if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                        if board.proof1(screen, i, j):
                            pygame.draw.rect(screen, (0, 200, 200), (i * 40, j * 40, 40, 40))
                            self.board[i][j] = 2
                            self.mouse_ship = False
                            self.num1 = str(int(self.num1) - 1)

    def de_single(self):  # удаляет единичку
        self.num1 = str(int(self.num1) + 1)
        for i in range(10):
            if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                for j in range(10):
                    if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                        self.board[i][j] = 0
                        if i > 0 and j > 0:
                            self.board[i - 1][j - 1] = 0
                        if j < 9 and i < 9:
                            self.board[i + 1][j + 1] = 0
                        if i > 0:
                            self.board[i - 1][j] = 0
                        if i < 9:
                            self.board[i + 1][j] = 0
                        if j < 9:
                            self.board[i][j + 1] = 0
                        if j > 0:
                            self.board[i][j - 1] = 0
                        if i < 9 and j > 0:
                            self.board[i + 1][j - 1] = 0
                        if i > 0 and j < 9:
                            self.board[i - 1][j + 1] = 0

    def set_double(self):
        for i in range(10):
            if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                for j in range(10):
                    if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                        for k in range(4):
                            pygame.draw.rect(screen, (0, 200, 200), ((i + k) * 40, j * 40, 40, 40))
                            self.x.append((i + k) * 40 + 10)
                            self.y.append(j * 40 + 10)

    def set_triple(self):
        pass

    def set_four(self):
        pass

    def set_ship(self):  # определяет размер кораблика
        if self.mouse_ship:  # определяет, был ли нажат кораблик
            if self.numberofcells == 1:
                self.set_single()
            if self.numberofcells == 2:
                self.set_double()
            if self.numberofcells == 3:
                self.set_triple()
            if self.numberofcells == 4:
                self.set_four()

    def get_cell(self, sc):  # вырисовывает нажатый курсорчик
        if self.mouse_ship:
            pygame.draw.rect(sc, (0, 100, 100), (event.pos[0], event.pos[1], 40, 40))

    def starting(self):  # запуск вторичного поля
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.board[i][j] = 0
        self.running = False
        self.stage2 = True

    def where_pressed(self, s):
        if event.pos[0] < 471 and event.pos[0] > 429:
            if event.pos[1] < 321 and event.pos[1] > 279:
                if self.num1 != '0':
                    self.numberofcells = 1
                    self.mouse_ship = True
        if s.get_at((event.pos[0], event.pos[1]))[:3] == (0, 100, 100):  # при нажатии на кораблик удаляет
            event0, event1 = event.pos[0] + 40, event.pos[1] - 40
            if event.pos[0] > 360:
                event0 = 0
            if event.pos[0] < 60:
                event0 = 0
            if event.pos[1] > 360:
                event1 = 0
            if event.pos[1] < 60:
                event1 = 0
            if s.get_at((event0, event1))[:3] != (0, 100, 100):
                if s.get_at((event0, event1))[:3] != (0, 100, 100):
                    if s.get_at((event0, event1))[:3] != (0, 100, 100):
                        if s.get_at((event0, event1))[:3] != (0, 100, 100):
                            self.de_single()
                        else:
                            pass
                    else:
                        pass
        self.set_ship()
        if s.get_at((event.pos[0], event.pos[1]))[:3] == (0, 255, 0):
            self.starting()


if __name__ == '__main__':
    size = width, height = 650, 420  # создание первичного поля (поле игрока)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игрок 1')

    board = Board()

    fps = 50
    clock = pygame.time.Clock()

    board.running = True
    while board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из окна
                exit()
            elif event.type == pygame.MOUSEMOTION:
                board.get_cell(screen)  # ведение курсорчика
                pygame.display.flip()
                screen.fill((0, 0, 0))
                board.render1(screen)  # создание поля
                board.ships(screen)  # заполнение кораблями
            elif event.type == pygame.MOUSEBUTTONUP:
                board.where_pressed(screen)  # проверяет, куда тыкнули
                screen.fill((0, 0, 0))
                board.render1(screen)  # создание поля
                board.ships(screen)  # заполнение кораблями
                pygame.display.flip()
            else:
                pass
        clock.tick(fps)

    screen = pygame.display.set_mode((840, 420))  # создание вторичного поля (там, где уже идёт игра)
    board.render2(screen)
    board.ships(screen)  # заполнение кораблями
    pygame.display.flip()

    board.running = True
    while board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            else:
                pass
        clock.tick(fps)
    pygame.quit()
