# Импорты библиотек
import pygame as pg
import typing as tp

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Частота кадров
FPS = 60

# Начальная карта игрового поля
INITIAL_FIELD_MAP = [[1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1]]

# Размер стороны клетки редактируемого поля
EDIT_SQUARE_SIDE_SIZE = 50

# Размер кнопки редактирования
EDIT_BUTTON_SIZE = (50, 50)

# Минимально допустимое количество клеток в строке или столбце поля
MIN_SQUARES_IN_ROW_AND_COLUMN = 3

# Ширина границы у выбранной клетки
SELECTED_EDIT_BUTTON_BORDER_WIDTH = 3

# Цвет границы у выбранной клетки
SELECTED_EDIT_BUTTON_BORDER_COLOR = (0, 0, 255)


class LevelEditor:
    """
    Класс для реализации редактора уровней.
    """
    
    @staticmethod
    def start(screen: pg.Surface) -> None:
        """
        Метод для запуска редактора уровней.

        :param screen: Экран игры.
        """

        # Абсолютные координаты экрана относительно карты уровня
        screen_absolute_coordinates = [0, 0]
        
        # Часы для регулировки FPS
        clock = pg.time.Clock()

        # Поверхность для отображения игрового поля
        screen_field = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Устанавливаем фон
        background = pg.image.load("design/level_editor/background.png")
        screen.blit(background, (0, 0))
        pg.display.update()

        # Создаём редактируемое игровое поле
        edit_field = EditField(screen, screen_field, background, screen_absolute_coordinates, INITIAL_FIELD_MAP)

        # Создаём контроллер для управления редактором уровней
        edit_controller = EditController()

        # Центрируем и отрисовываем игровое поле
        edit_field.center()
        edit_field.update()

        # Запускаем цикл работы редактора
        while True:
            
            # Регулируем FPS
            clock.tick(FPS)

            # Перебираем игровые события
            for e in pg.event.get():

                # При закрытии игрового окна завершаем программу
                if e.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    
                    # Получаем координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Получаем кликнутый объект
                    clicked_object = edit_field.get_clicked_object(click_coordinates[0], click_coordinates[1])

                    # если кликнутого объекта нет, то пропускаем итерацию
                    if clicked_object is None:
                        continue

                    # Если клик пришёлся на кнопку редактирования поля
                    elif isinstance(clicked_object, EditButton):

                        # Получаем кликнутую кнопку
                        clicked_button = clicked_object
                        
                        # Если кликнута кнопка увеличения стороны поля, то увеличиваем эту сторону и обновляем поле
                        if clicked_button.button_type == "add":
                            edit_field.increase_side(clicked_button.side_type)
                            edit_field.update()
                            continue

                        # Если кликнута кнопка уменьшения стороны поля, то уменьшаем эту сторону и обновляем поле
                        elif clicked_button.button_type == "delete":
                            edit_field.decrease_side(clicked_button.side_type)
                            edit_field.update()
                            continue

                    # Если клик пришёлся на клетку поля
                    elif isinstance(clicked_object, EditSquare):
                        
                        # Получаем кликнутую клетку
                        clicked_square = clicked_object

                        # Если кликнутая клетка уже была выбрана ранее, то снимаем с неё выделение и обновляем поле
                        if clicked_square == edit_controller.selected_square:
                            clicked_square.deselect()
                            edit_controller.selected_square = None
                            edit_field.update()
                            continue

                        # Если кликнутая клетка не была выбрана ранее, то снимаем выделение с предыдущей выбранной 
                        # клетки (если она не равна None) и делаем выбранной кликнутую клетку и обновляем поле
                        elif clicked_square != edit_controller.selected_square:
                            if edit_controller.selected_square is not None:
                                edit_controller.selected_square.deselect()
                            clicked_square.select()
                            edit_controller.selected_square = clicked_square
                            edit_field.update()
                            continue

                # Если нажата правая клавиша мыши, то ставим флаг движения карты и флаг для пропуска первого сдвига
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
                    edit_field.is_moving = True
                    edit_field.skip_first_move = True
                
                # Если отпущена правая клавиша мыши, то снимаем флаг движения карты и флаг пропуска первого сдвига
                elif e.type == pg.MOUSEBUTTONUP and e.button == 3:
                    edit_field.is_moving = False
                    edit_field.skip_first_move = False

                # Если мышь движется с установленным флагом движения карты
                elif e.type == pg.MOUSEMOTION and edit_field.is_moving:

                    # Находим сдвиг курсора по x и y
                    mouse_shift = pg.mouse.get_rel()
                    x_shift = mouse_shift[0]
                    y_shift = mouse_shift[1]

                    # Если у поля стоит флаг пропуска первого сдвига, то снимаем данный флаг и пропускаем итерацию
                    if edit_field.skip_first_move:
                        edit_field.skip_first_move = False
                        continue

                    # Сдвигаем игровое поле и обновляем его
                    edit_field.move(x_shift, y_shift)
                    edit_field.update()


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
            surface = pg.image.load("./design/level_editor/add_button.png")
            self.image.blit(surface, (0, 0))
        
        # Кнопка уменьшения стороны
        elif self.button_type == "delete":
            surface = pg.image.load("./design/level_editor/delete_button.png")
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
    
    def __init__(self, x: int, y: int, field: LevelEditor) -> None:
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
        self.image = pg.image.load("./design/level_editor/square.png")

        # Задаём область клетки, основываясь на переданных координатах
        self.rect = pg.Rect(x, y, self.side_size, self.side_size)

        # Флаг, показывающий выбрана ли клетка
        self.is_selected = False

    def update(self) -> None:
        """
        Функция для обновления клетки. 
        """
        
        # Загружаем базовый вариант клетки
        self.image = pg.image.load("design/field/square.png")

        # Если клетка выбрана, то рисуем вокруг неё рамку
        if self.is_selected:
            surface = pg.Surface((self.side_size, self.side_size), pg.SRCALPHA)
            pg.draw.rect(surface, 
                              SELECTED_EDIT_BUTTON_BORDER_COLOR, 
                              (0, 0, self.side_size, self.side_size), 
                              SELECTED_EDIT_BUTTON_BORDER_WIDTH)
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


class EditField:
    """
    Класс для реализации редактируемого игрового поля.
    """
    
    def __init__(self,
                 screen: pg.Surface,
                 screen_field: pg.Surface,
                 background: pg.Surface,
                 screen_absolute_coordinates: list[int],
                 initial_field_map: list[list[int]]) -> None:
        """
        Функция для инициализации поля.

        :param screen: Экран игры.
        :param screen_field: Поверхность для отображения поля.
        :param background: Задний фон поля.
        :param screen_absolute_coordinates: Абсолютные координаты экрана относительно поля.
        :param initial_field_map: Начальная карта игрового поля.
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

    def get_square_side_size(self) -> int:
        """
        Функция, возвращающая размер стороны клетки игрового поля.

        :return: Текущий размер клетки игрового поля.
        """

        # Возвращаем размер стороны первой клетки в списке с игровыми клетками
        # (т.к. все клетки имеют одинаковый размер)
        return self.squares_list[0][0].rect.width

    def get_field_width(self) -> int:
        """
        Функция, возвращающая ширину игрового поля.

        :return: Ширина игрового поля.
        """

        # Рассчитываем и возвращаем ширину игрового поля
        return len(self.squares_list[0]) * self.get_square_side_size()

    def get_field_height(self) -> int:
        """
        Функция, возвращающая высоту игрового поля.

        :return: Высота игрового поля.
        """

        # Рассчитываем и возвращаем высоту игрового поля
        return len(self.squares_list) * self.get_square_side_size()

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
        square_side_size = self.get_square_side_size()

        # Получаем размеры экрана
        screen_width = self.screen_field.get_width()
        screen_height = self.screen_field.get_height()

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

    def get_clicked_object(self, x: int, y: int) -> tp.Union[EditSquare, EditButton, None]:
        """
        Функция для получения кликнутого объекта.

        :param x: Координата клика по x.
        :param y: Координата клика по y.

        :return: Кликнутый объект или None, если кликнутого объекта не найдено.
        """
        
        # Перебираем все клетки и если клик пришёлся на какую-то клетку, то возвращаем её
        for square in self.squares_group:
            if square.rect.collidepoint(x, y):
                return square
        
        # Перебираем все кнопки редактирования и если клик пришёлся на какую-то кнопку, то возвращаем её
        for edit_button in self.edit_buttons_group:
            if edit_button.rect.collidepoint(x, y):
                return edit_button
        
        # Иначе возвращаем None
        return None

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


class EditInterface:
    """
    Класс для реализации интерфейса редактирования.
    """
    pass


class EditInterfaceButton:
    """
    Класс для реализации кнопки интерфейса редактирования.
    """
    pass


class EditController:
    """
    Класс для реализации контроллера для управления редактором уровней.
    """
    
    def __init__(self) -> None:
        """
        Функция для инициализации контроллера редактирования.
        """
        
        # Текущая выбранная клетка
        self.selected_square: tp.Union[EditSquare, None] = None


# Область для отладки
if __name__ == "__main__":
    pass
