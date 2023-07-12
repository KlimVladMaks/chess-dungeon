# Импорт библиотек
import pygame as pg
import typing as tp

# Импорт файлов для задания типов
if tp.TYPE_CHECKING:
    from level_editor.level_editor import LevelEditor
    from level_editor.edit_menu import EditMenu

# Размер стороны клетки редактируемого поля
EDIT_SQUARE_SIDE_SIZE = 50

# Размер кнопки редактирования
EDIT_BUTTON_SIZE = (50, 50)

# Минимально допустимое количество клеток в строке или столбце поля
MIN_SQUARES_IN_ROW_AND_COLUMN = 3

# Ширина границы у выбранной клетки
SELECTED_EDIT_SQUARE_BORDER_WIDTH = 3

# Цвет границы у выбранной клетки
SELECTED_EDIT_SQUARE_BORDER_COLOR = (0, 0, 255)

# Цвет заливки у выбранной клетки
SELECTED_EDIT_SQUARE_FILL_COLOR = (0, 0, 255, 20)


class EditButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки редактирования поля (увеличения или уменьшения поля).
    """
    
    def __init__(self, x: int, y: int, button_type: str, side_type: str) -> None:
        """
        Функция для инициализации кнопки редактирования.

        :param x: Координата x кнопки.
        :param y: Координата y кнопки.
        :param button_type: Тип кнопки ("add", "delete").
        :param side_type: Тип стороны, с которой работает кнопка ("top", "right", "bottom", "left").
        """

        # Инициализируем спрайт кнопки
        pg.sprite.Sprite.__init__(self)

        # Сохраняем тип кнопки
        self.button_type = button_type

        # Сохраняем тип стороны, с которой работает кнопка
        self.side_type = side_type

        # Создаём поверхность кнопки
        self.image = pg.Surface(EDIT_BUTTON_SIZE)

        # Создаём область кнопки
        self.rect = pg.Rect(x, y, EDIT_BUTTON_SIZE[0], EDIT_BUTTON_SIZE[1])

        # Отрисовываем кнопку
        self.update()

    def update(self) -> None:
        """
        Функция для отрисовки кнопки редактирования.
        """
        
        # Кнопка увеличения стороны
        if self.button_type == "add":
            surface = pg.image.load("./design/level_editor/edit_field/add_button.png")
            self.image.blit(surface, (0, 0))
        
        # Кнопка уменьшения стороны
        elif self.button_type == "delete":
            surface = pg.image.load("./design/level_editor/edit_field/delete_button.png")
            self.image.blit(surface, (0, 0))

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига позиции кнопки редактирования.

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Сдвигаем область клетки на заданные координатные сдвиги
        self.rect.move_ip(x_shift, y_shift)


class EditSquare(pg.sprite.Sprite):
    """
    Класс для реализации клетки на редактируемом поле.
    """
    
    def __init__(self, x: int, y: int, field: 'LevelEditor') -> None:
        """
        Функция для инициализации клетки редактируемого поля.

        :param x: Начальная координата x клетки.
        :param y: Начальная координата y клетки.
        :param field: Игровое поле.
        """
        
        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем игровое поле
        self.field = field

        # Сохраняем размер стороны клетки
        self.side_size = EDIT_SQUARE_SIDE_SIZE

        # Загружаем базовое изображение поверхности клетки
        self.image = pg.image.load("./design/field/square.png")

        # Задаём область клетки, основываясь на переданных координатах
        self.rect = pg.Rect(x, y, self.side_size, self.side_size)

        # Флаг, показывающий выбрана ли клетка
        self.is_selected = False

        # Тип клетки
        self.square_type = "square"

    def update(self) -> None:
        """
        Функция для обновления клетки. 
        """

        # Задаём клетке базовый дизайн
        self.image = pg.image.load("./design/level_editor/edit_square/square.png")
        
        # Задаём дизайн клетке в зависимости от её типа
        try:
            surface = pg.image.load(f"./design/level_editor/edit_square/{self.square_type}.png")
            self.image.blit(surface, (0, 0))
        except:
            pass

        # Если клетка выбрана, то рисуем вокруг неё рамку и делаем заливку
        if self.is_selected:
            surface = pg.Surface((self.side_size, self.side_size), pg.SRCALPHA)
            surface.fill(SELECTED_EDIT_SQUARE_FILL_COLOR)
            self.image.blit(surface, (0, 0))
            surface = pg.Surface((self.side_size, self.side_size), pg.SRCALPHA)
            pg.draw.rect(surface, 
                              SELECTED_EDIT_SQUARE_BORDER_COLOR, 
                              (0, 0, self.side_size, self.side_size), 
                              SELECTED_EDIT_SQUARE_BORDER_WIDTH)
            self.image.blit(surface, (0, 0))

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига позиции клетки.

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Сдвигаем область клетки на заданные координатные сдвиги
        self.rect.move_ip(x_shift, y_shift)

    def toggle_select(self) -> None:
        """
        Функция для переключения клетки в выбранный/невыбранный режим.
        """
        
        # Если клетка выбрана, то снимаем флаг выбора, иначе ставим флаг выбора
        if self.is_selected:
            self.is_selected = False
        else:
            self.is_selected = True

        # Обновляем клетку
        self.update()

    def select(self) -> None:
        """
        Функция для перевода клетки в выбранный режим.
        """
        
        # Ставим флаг выбора и обновляем клетку
        self.is_selected = True
        self.update()

    def deselect(self) -> None:
        """
        Функция для перевода клетки в невыбранный режим.
        """
        
        # Снимаем флаг выбора и обновляем клетку
        self.is_selected = False
        self.update()

    def set_barrier(self) -> None:
        """
        Функция, превращающая клетку в барьер.
        """

        # Задаём клетки тип барьера и обновляем её
        self.square_type = "barrier"
        self.update()

    def set_square(self) -> None:
        """
        Функция для превращения клетки в обычную клетку.
        """
        
        # Задаём клетки тип обычной клетки и обновляем её
        self.square_type = "square"
        self.update()

    def get_pos(self) -> tuple[int, int]:
        """
        Функция для получения позиции клетки на карте поля.
        """
        
        # Перебираем позиции всех клеток на карте поля и при совпадении возвращаем позицию данной клетки
        for i in range(len(self.field.squares_list)):
            for j in range(len(self.field.squares_list[i])):
                if self.field.squares_list[i][j] == self:
                    return i, j


class EditField:
    """
    Класс для реализации редактируемого игрового поля.
    """
    
    def __init__(self,
                 screen: pg.Surface,
                 screen_field: pg.Surface,
                 background: pg.Surface,
                 screen_absolute_coordinates: list[int],
                 initial_field_map: list[list[int]],
                 edit_menu: 'EditMenu') -> None:
        """
        Функция для инициализации поля.

        :param screen: Экран игры.
        :param screen_field: Поверхность для отображения поля.
        :param background: Задний фон поля.
        :param screen_absolute_coordinates: Абсолютные координаты экрана относительно поля.
        :param initial_field_map: Начальная карта игрового поля.
        :param edit_controller: Контроллер для управления редактированием.
        :param edit_menu: Меню редактора уровней.
        """
        
        # Сохраняем экран игры
        self.screen = screen

        # Сохраняем поверхность для отображения поля
        self.screen_field = screen_field

        # Сохраняем задний фон
        self.background = background

        # Сохраняем абсолютные координаты экрана относительно поля
        self.screen_absolute_coordinates = screen_absolute_coordinates

        # Сохраняем копию начальной карты поля
        self.field_map = initial_field_map.copy()

        # Сохраняем меню редактора уровней
        self.edit_menu = edit_menu

        # Двухмерный список для хранения спрайтов шахматных клеток
        self.squares_list: list[list[EditSquare]] = []

        # Группа для хранения спрайтов шахматных клеток
        self.squares_group = pg.sprite.Group()

        # Извлекаем координаты начала экрана
        x = -self.screen_absolute_coordinates[0]
        y = -self.screen_absolute_coordinates[1]

        # Задаём структуру игрового поля, заполняя его клетками в соответствии с картой поля
        # (Заполняем список и группу клеток)
        for row in self.field_map:
            inner_list = []
            for col in row:
                if col == 1:
                    square = EditSquare(x, y, self)
                    self.squares_group.add(square)
                    inner_list.append(square)
                x += EDIT_SQUARE_SIDE_SIZE
            y += EDIT_SQUARE_SIDE_SIZE
            x = -self.screen_absolute_coordinates[0]
            self.squares_list.append(inner_list)
        
        # Добавляем к полю кнопки редактирования
        self.add_edit_buttons()

        # Флаг движения игрового поля
        self.is_moving = False

        # Флаг скрытия первого сдвига при движении игрового поля
        self.skip_first_move = False

    def update(self) -> None:
        """
        Функция для обновления (перерисовки) игрового поля.
        """

        # Перерисовываем игровое поле
        self.screen_field.blit(self.background, (0, 0))
        self.squares_group.draw(self.screen_field)
        self.edit_buttons_group.draw(self.screen_field)
        self.screen.blit(self.screen_field, (0, 0))

        # Отрисовываем кнопку открытия меню редактора уровней
        self.screen_field.blit(self.edit_menu.open_menu_button.image, self.edit_menu.open_menu_button.rect)
        self.screen.blit(self.screen_field, (0, 0))

        # Обновляем экран
        pg.display.update()

    def add_edit_buttons(self) -> None:
        """
        Функция для добавления кнопок редактирования (уменьшения и увеличения поля).
        """
        
        # Создаём группу для спрайтов кнопок увеличения и уменьшения сторон поля
        self.edit_buttons_group = pg.sprite.Group()

        # Задаём верхнюю пару кнопок редактирования
        x = -self.screen_absolute_coordinates[0] + (self.get_field_width() // 2) - EDIT_BUTTON_SIZE[0]
        y = -self.screen_absolute_coordinates[1] - EDIT_BUTTON_SIZE[1] - (EDIT_BUTTON_SIZE[1] // 2)
        edit_button = EditButton(x, y, "add", "top")
        self.edit_buttons_group.add(edit_button)
        x += EDIT_BUTTON_SIZE[0]
        edit_button = EditButton(x, y, "delete", "top")
        self.edit_buttons_group.add(edit_button)

        # Задаём правую пару кнопок редактирования
        x = -self.screen_absolute_coordinates[0] + self.get_field_width() + (EDIT_BUTTON_SIZE[0] // 2)
        y = -self.screen_absolute_coordinates[1] + (self.get_field_height() // 2) - EDIT_BUTTON_SIZE[1]
        edit_button = EditButton(x, y, "add", "right")
        self.edit_buttons_group.add(edit_button)
        y += EDIT_BUTTON_SIZE[1]
        edit_button = EditButton(x, y, "delete", "right")
        self.edit_buttons_group.add(edit_button)

        # Задаём нижнюю пару кнопок редактирования
        x = -self.screen_absolute_coordinates[0] + (self.get_field_width() // 2) - EDIT_BUTTON_SIZE[0]
        y = -self.screen_absolute_coordinates[1] + self.get_field_height() + (EDIT_BUTTON_SIZE[1] // 2)
        edit_button = EditButton(x, y, "add", "bottom")
        self.edit_buttons_group.add(edit_button)
        x += EDIT_BUTTON_SIZE[0]
        edit_button = EditButton(x, y, "delete", "bottom")
        self.edit_buttons_group.add(edit_button)

        # Задаём левую пару кнопок редактирования
        x = -self.screen_absolute_coordinates[0] - (EDIT_BUTTON_SIZE[0] // 2) - EDIT_BUTTON_SIZE[0]
        y = -self.screen_absolute_coordinates[1] + (self.get_field_height() // 2) - EDIT_BUTTON_SIZE[1]
        edit_button = EditButton(x, y, "add", "left")
        self.edit_buttons_group.add(edit_button)
        y += EDIT_BUTTON_SIZE[1]
        edit_button = EditButton(x, y, "delete", "left")
        self.edit_buttons_group.add(edit_button)

    def get_field_width(self) -> int:
        """
        Функция, возвращающая ширину игрового поля.

        :return: Ширина игрового поля.
        """

        # Рассчитываем и возвращаем ширину игрового поля
        return len(self.squares_list[0]) * EDIT_SQUARE_SIDE_SIZE

    def get_field_height(self) -> int:
        """
        Функция, возвращающая высоту игрового поля.

        :return: Высота игрового поля.
        """

        # Рассчитываем и возвращаем высоту игрового поля
        return len(self.squares_list) * EDIT_SQUARE_SIDE_SIZE

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига игрового поля.
        (Функция не даёт игровому полю выйти за пределы экрана более чем наполовину).

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Рассчитываем потенциальные новые абсолютные координаты экрана
        x_screen_test = self.screen_absolute_coordinates[0] - x_shift
        y_screen_test = self.screen_absolute_coordinates[1] - y_shift

        # Рассчитываем размеры поля
        field_width = self.get_field_width()
        field_height = self.get_field_height()

        # Получаем размеры одной клетки
        square_side_size = EDIT_SQUARE_SIDE_SIZE

        # Получаем размеры экрана
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Если при сдвиге по X на экран не попадает ни одной целой клетки, то обнуляем сдвиг по X
        if (x_screen_test < -(screen_width - square_side_size)) or \
           (x_screen_test > (field_width - square_side_size)):
            x_shift = 0
        
        # Если при сдвиге по Y на экран не попадает ни одной целой клетки, то обнуляем сдвиг по Y
        if (y_screen_test < -(screen_height - square_side_size)) or \
           (y_screen_test > (field_height - square_side_size)):
            y_shift = 0

        # Сдвигаем каждую клетку игрового поля
        for square in self.squares_group:
            square.move(x_shift, y_shift)
        
        # Сдвигаем кнопки редактирования
        for edit_button in self.edit_buttons_group:
            edit_button.move(x_shift, y_shift)

        # Обновляем абсолютные координаты экрана
        self.screen_absolute_coordinates[0] -= x_shift
        self.screen_absolute_coordinates[1] -= y_shift

    def center(self) -> None:
        """
        Функция для перемещения поля в центр экрана.
        """
        
        # Рассчитываем размеры поля
        field_width = self.get_field_width()
        field_height = self.get_field_height()

        # Получаем размеры экрана
        screen_width = self.screen_field.get_width()
        screen_height = self.screen_field.get_height()

        # Находим сдвиги, необходимые для центрирования поля
        x_shift = ((screen_width // 2) - (field_width // 2)) - self.screen_absolute_coordinates[0]
        y_shift = ((screen_height // 2) - (field_height // 2)) - self.screen_absolute_coordinates[1]

        # Перемещаем поле в центр экрана
        self.move(x_shift, y_shift)

    def get_object_by_coordinates(self, x: int, y: int) -> tp.Union[EditSquare, EditButton, 'EditMenu', None]:
        """
        Функция для получения объекта по его координатам.

        :param x: Координата x.
        :param y: Координата y.

        :return: Объект с заданными координатами или None, если объекта не найдено.
        """

        # Если нажата кнопка открытия меню редактора уровней, то возвращаем меню редактора уровней
        if self.edit_menu.is_open_button_clicked((x, y)):
            return self.edit_menu
        
        # Перебираем все кнопки редактирования и если координаты попадают на какую-то кнопку, то возвращаем её
        for edit_button in self.edit_buttons_group:
            if edit_button.rect.collidepoint(x, y):
                return edit_button
        
        # Рассчитываем абсолютные координаты клетки
        x_absolute = x + self.screen_absolute_coordinates[0]
        y_absolute = y + self.screen_absolute_coordinates[1]

        # Получаем размер стороны клетки
        square_side_size = EDIT_SQUARE_SIDE_SIZE

        # Если абсолютные x или y меньше 0, то возвращаем None
        if x_absolute < 0 or y_absolute < 0:
            return None

        # Отлавливаем ошибки для избежания выхода из диапазона
        try:

            # Рассчитываем позицию клетки и извлекаем её из двухмерного списка клеток
            square_col = x_absolute // square_side_size
            square_row = y_absolute // square_side_size
            found_square = self.squares_list[square_row][square_col]

        # При выходе из диапазона возвращаем None
        except IndexError:
            return None

        # Возвращаем найденную клетку
        return found_square

    def get_pos_by_square(self, square: EditSquare) -> tuple[int, int]:
        """
        Функция, возвращающая позицию переданной клетки в списке клеток игрового поля.

        :param square: Клетка игрового поля.
        :return: Позиция клетки в списке клеток игрового поля.
        """

        # Находим и возвращаем позицию клетки в списке клеток игрового поля
        for i in range(len(self.squares_list)):
            for j in range(len(self.squares_list[i])):
                if self.squares_list[i][j] == square:
                    return i, j

    def increase_side(self, side_type: str) -> None:
        """
        Функция для увеличения одной из сторон поля.

        :param side_type: Тип стороны поля, которую нужно увеличить ("top", "right", "bottom", "left").
        """
        
        # Если нужно увеличить верхнюю сторону поля
        if side_type == "top":
            
            # Обновляем карту поля
            top_row_list = [1 for _ in range(len(self.squares_list[0]))]
            self.field_map.insert(0, top_row_list)

            # Добавляем клетки из верхнего ряда в список и группу клеток
            x = self.squares_list[0][0].rect.x
            y = self.squares_list[0][0].rect.y - EDIT_SQUARE_SIDE_SIZE
            top_row_square_list: list[EditSquare] = []
            for _ in range(len(self.squares_list[0])):
                square = EditSquare(x, y, self)
                top_row_square_list.append(square)
                self.squares_group.add(square)
                x += EDIT_SQUARE_SIDE_SIZE
            self.squares_list.insert(0, top_row_square_list)

            # Обновляем абсолютные координаты экрана
            self.screen_absolute_coordinates[1] += EDIT_SQUARE_SIDE_SIZE

            # Сдвигаем поле для выравнивания
            self.move(0, EDIT_SQUARE_SIDE_SIZE)

        # Если нужно увеличить правую сторону поля
        elif side_type == "right":
            
            # Обновляем карту поля
            for row_list in self.field_map:
                row_list.append(1)
            
            # Добавляем клетки из правого столбца в список и группу клеток
            x = self.squares_list[0][-1].rect.x + EDIT_SQUARE_SIDE_SIZE
            y = self.squares_list[0][-1].rect.y
            for square_row in self.squares_list:
                square = EditSquare(x, y, self)
                square_row.append(square)
                self.squares_group.add(square)
                y += EDIT_SQUARE_SIDE_SIZE
            
            # Сдвигаем поле для выравнивания
            self.move(-EDIT_SQUARE_SIDE_SIZE, 0)

        # Если нужно увеличить нижнюю сторону поля
        elif side_type == "bottom":

            # Обновляем карту поля
            bottom_row_list = [1 for _ in range(len(self.squares_list[0]))]
            self.field_map.append(bottom_row_list)

            # Добавляем клетки из нижнего ряда в список и группу клеток
            x = self.squares_list[-1][0].rect.x
            y = self.squares_list[-1][0].rect.y + EDIT_SQUARE_SIDE_SIZE
            bottom_row_square_list: list[EditSquare] = []
            for _ in range(len(self.squares_list[-1])):
                square = EditSquare(x, y, self)
                bottom_row_square_list.append(square)
                self.squares_group.add(square)
                x += EDIT_SQUARE_SIDE_SIZE
            self.squares_list.append(bottom_row_square_list)

            # Сдвигаем поле для выравнивания
            self.move(0, -EDIT_SQUARE_SIDE_SIZE)

        # Если нужно увеличить левую сторону поля
        elif side_type == "left":
            
            # Обновляем карту поля
            for row_list in self.field_map:
                row_list.append(1)
            
            # Добавляем клетки из левого столбца в список и группу клеток
            x = self.squares_list[0][0].rect.x - EDIT_SQUARE_SIDE_SIZE
            y = self.squares_list[0][0].rect.y
            for square_row in self.squares_list:
                square = EditSquare(x, y, self)
                square_row.insert(0, square)
                self.squares_group.add(square)
                y += EDIT_SQUARE_SIDE_SIZE
            
            # Обновляем абсолютные координаты экрана
            self.screen_absolute_coordinates[0] += EDIT_SQUARE_SIDE_SIZE

            # Сдвигаем поле для выравнивания
            self.move(EDIT_SQUARE_SIDE_SIZE, 0)

        # Добавляем кнопки редактирования к увеличенному полю
        self.add_edit_buttons()

    def decrease_side(self, side_type: str) -> None:
        """
        Функция для уменьшения одной из сторон поля.

        :param side_type: Тип стороны поля, которую нужно уменьшить ("top", "right", "bottom", "left").
        """

        # Если поле слишком маленькое для дальнейшего уменьшения, то завершаем функцию
        if ((side_type == "top" or side_type == "bottom") and len(self.field_map) <= MIN_SQUARES_IN_ROW_AND_COLUMN) or \
           ((side_type == "right" or side_type == "left") and len(self.field_map[0]) <= MIN_SQUARES_IN_ROW_AND_COLUMN):
            return

        # Если нужно уменьшить верхнюю сторону поля
        if side_type == "top":
            
            # Обновляем карту поля
            self.field_map.pop(0)

            # Удаляем клетки из верхнего ряда из списка и группы клеток
            top_row_square_list = self.squares_list.pop(0)
            for square in top_row_square_list:
                self.squares_group.remove(square)
            
            # Обновляем абсолютные координаты экрана
            self.screen_absolute_coordinates[1] -= EDIT_SQUARE_SIDE_SIZE

            # Сдвигаем поле
            self.move(0, -EDIT_SQUARE_SIDE_SIZE)

        # Если нужно уменьшить правую сторону поля
        elif side_type == "right":
            
            # Обновляем карту поля
            for row_list in self.field_map:
                row_list.pop(-1)
            
            # Удаляем клетки из правого столбца из списка и группы клеток
            for square_row in self.squares_list:
                square = square_row.pop(-1)
                self.squares_group.remove(square)

            # Сдвигаем поле
            self.move(EDIT_SQUARE_SIDE_SIZE, 0)

        # Если нужно уменьшить нижнюю сторону поля
        elif side_type == "bottom":
            
            # Обновляем карту поля
            self.field_map.pop(-1)

            # Удаляем клетки из нижнего ряда из списка и группы клеток
            bottom_row_square_list = self.squares_list.pop(-1)
            for square in bottom_row_square_list:
                self.squares_group.remove(square)

            # Сдвигаем поле
            self.move(0, EDIT_SQUARE_SIDE_SIZE)

        # Если нужно уменьшить левую сторону поля
        elif side_type == "left":
            
            # Обновляем карту поля
            for row_list in self.field_map:
                row_list.pop(0)
            
            # Удаляем клетки из левого столбца из списка и группы клеток
            for square_row in self.squares_list:
                square = square_row.pop(0)
                self.squares_group.remove(square)
            
            # Обновляем абсолютные координаты экрана
            self.screen_absolute_coordinates[0] -= EDIT_SQUARE_SIDE_SIZE
            
            # Сдвигаем поле
            self.move(-EDIT_SQUARE_SIDE_SIZE, 0)
        
        # Добавляем кнопки редактирования к уменьшенному полю
        self.add_edit_buttons()


# Область для отладки
if __name__ == "__main__":
    pass
