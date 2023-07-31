import pygame as pg


class Controls:
    """
    Класс для проверки игрового события на то, к какому действию оно относится.
    """
    
    @staticmethod
    def is_quit(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие выходом из игры.

        :param event: Событие.
        :return: True - если событие является выходом из игры, False - если нет.
        """

        return (event.type == pg.QUIT)

    @staticmethod
    def is_selection(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие выбором.

        :param event: Событие.
        :return: True - если событие является выбором, False - если нет.
        """
        
        return (event.type == pg.MOUSEBUTTONDOWN and event.button == 1)

    @staticmethod
    def is_stop_selection(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие прекращением выбора.

        :param event: Событие.
        :return: True - если событие является прекращением выбора, False - если нет.
        """

        return (event.type == pg.MOUSEBUTTONUP and event.button == 1)

    @staticmethod
    def is_next_move(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие переходом к следующему ходу.

        :param event: Событие.
        :return: True - если событие является переходом к следующему ходу, False - если нет.
        """

        return (event.type == pg.KEYDOWN and event.key == pg.K_RETURN)

    @staticmethod
    def is_start_map_shift(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие началом сдвига карты.

        :param event: Событие.
        :return: True - если событие является началом сдвига карты, False - если нет.
        """

        return (event.type == pg.MOUSEBUTTONDOWN and event.button == 2)

    @staticmethod
    def is_cursor_motion(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие перемещением курсора.

        :param event: Событие.
        :return: True - если событие является перемещением курсора, False - если нет.
        """

        return (event.type == pg.MOUSEMOTION)

    @staticmethod
    def is_stop_map_shift(event: pg.event.Event) -> bool:
        """
        Функция для проверки того, является ли событие прекращением сдвига карты.

        :param event: Событие.
        :return: True - если событие является прекращением сдвига карты, False - если нет.
        """

        return (event.type == pg.MOUSEBUTTONUP and event.button == 2)
