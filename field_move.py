import pygame

pygame.init()
width = 320 * 3
height = 180 * 3
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

start_field = [0, 0]
start_move_field = False
cell_size = 50

firld_widht = 20
firld_height = 20
field = [[1]*firld_widht for _ in range(firld_height)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    screen.fill("purple")

    for i in range(len(field)):
        for j in range(len(field[0])):
            pygame.draw.rect(screen, "blue", pygame.Rect(j*cell_size + start_field[0], i*cell_size + start_field[1], cell_size-1, cell_size-1))

    pygame.display.flip()

    press_mouse = pygame.mouse.get_pressed()

    if press_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        j = (mouse_pos[0] - start_field[0]) // cell_size
        i = (mouse_pos[1] - start_field[1]) // cell_size
        print(i, j)

    if press_mouse[2]:
        if not start_move_field:
            start_move_field = True
            pygame.mouse.get_rel()
        change_mouse_pos = pygame.mouse.get_rel()
        print(start_field)

        start_field[0] += change_mouse_pos[0]
        if start_field[0] >= 100:
            start_field[0] = 100
        elif start_field[0] <= width - cell_size * firld_widht - 100:
            start_field[0] = width - cell_size * firld_widht - 100

        start_field[1] += change_mouse_pos[1]
        if start_field[1] >= 100:
            start_field[1] = 100
        elif start_field[1] <= height - cell_size * firld_height - 100:
            start_field[1] = height - cell_size * firld_height - 100

    if not press_mouse[2] and start_move_field:
        start_move_field = False

    clock.tick(60)

pygame.quit()