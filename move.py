import typing as tp

#Списки условных обозначений, являющиеся стеной
WALLS = [0]

class Piece():

    def __init__(self, field, pos: tuple, move: int):
        """
        Пока что фигура хранит копию поля, чтобы обращаться к состаянию клеток
        """

        self.field = field #копия карты
        self.pos = pos #положение клетки
        self.move = move #радиус обзора

    def get_cell(self, x: int, y: int):
        """
        Функция возвращает состояние запращиваемой клетки
        """
        return self.field[x][y]

    def is_wall(self, x: int, y: int) -> bool:

        """
        Функция проверяет, является ли иходная клетка стеной
        (стена - любая клетка преграждающая обзор)

        """
        cell = self.get_cell(x, y)

        if cell in WALLS:
            return True
    
        return False

    def get_move(self):
        """
        Функция возвращает все клетки до которых можно дойти
        Работает это через обход в ширину со стартовой клетки
        """

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        i = 0
        cells = []
        len_way = []

        #проверим о выходе за пределы массива
        if (self.pos[1] >= 0
            and self.pos[1] < len(self.field)
                and self.pos[0] >= 0
                    and self.pos[0] < len(self.field[0])):
            cells.append((self.pos[1], self.pos[0]))
            len_way.append(0)

        while i < len(cells):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива
            if (not (cells[i][0] + 1, cells[i][1]) in cells
                    and len_way[i] < self.move
                        and cells[i][0] + 1 >= 0
                            and cells[i][0] + 1 < len(self.field)
                                and cells[i][1] >= 0
                                    and cells[i][1] < len(self.field[0])
                                        and not self.is_wall(cells[i][0] + 1, cells[i][1])):
                cells.append((cells[i][0] + 1, cells[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (cells[i][0] - 1, cells[i][1]) in cells
                    and len_way[i] < self.move
                        and cells[i][0] - 1 >= 0
                            and cells[i][0] - 1 < len(self.field)
                                and cells[i][1] >= 0
                                    and cells[i][1] < len(self.field[0])
                                        and not self.is_wall(cells[i][0] - 1, cells[i][1])):
                cells.append((cells[i][0] - 1, cells[i][1]))
                len_way.append(len_way[i] + 1)
            
            if (not (cells[i][0], cells[i][1] + 1) in cells
                    and len_way[i] < self.move
                        and cells[i][0] >= 0
                            and cells[i][0] < len(self.field)
                                and cells[i][1] + 1 >=0
                                    and cells[i][1] + 1 < len(self.field[0])
                                        and not self.is_wall(cells[i][0], cells[i][1] + 1)):
                cells.append((cells[i][0], cells[i][1] + 1))
                len_way.append(len_way[i] + 1)

            if (not (cells[i][0], cells[i][1] - 1) in cells
                    and len_way[i] < self.move
                        and cells[i][0] >= 0
                            and cells[i][0] < len(self.field)
                                and cells[i][1] - 1 >=0
                                    and cells[i][1] - 1 < len(self.field[0])
                                        and not self.is_wall(cells[i][0], cells[i][1] - 1)):
                cells.append((cells[i][0], cells[i][1] - 1))
                len_way.append(len_way[i] + 1)

            #переходим к следующему элементу
            i += 1

        return cells

if __name__ == '__main__':
    
    level_map = [
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]
    
    a = Piece(level_map, (9, 9), 3)

    b = a.get_move()

    print(b, len(b))