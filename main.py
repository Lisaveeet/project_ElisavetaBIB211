import pygame
from classes import all_objects, DefaultTank, DefaultWall
from random import randint, choice


FPS = 60#задержка между обновлениями в милисекундах


pygame.init()# создаём "Холст" Pygam'a
pygame.mouse.set_visible(False)# делаем курсор невидимым
pygame.display.set_caption("Tanks Offline")# делаем название экрана Tanks Offline
screen = pygame.display.set_mode((1000, 700)) # делаем размер экрана
clock = pygame.time.Clock()# создаём таймер для задержки 


p1 = DefaultTank(100, 100, (1, 0), (0, 255, 0))# создаём танк на координатах 100px 100px  с направленем 1 по x и 0 по y."Цвет" зелёный
p1.set_controls(pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE)#делаем управление w -- вверх,K -- вниз и т.д.
p2 = DefaultTank(900, 600, (-1, 0), (255, 0, 255))#создаём танк на координатах 900px 600px  с направленем -1 по x и 0 по y."Цвет" пурпурный

p2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_KP0)#аналог прошлому танку


#for _ in range(5):
#    DefaultWall(randint(50, 950), randint(50, 700), 20, randint(200, 600), (0, 150, 0)) #рандомно генерируем стену рандомного размера
#    DefaultWall(randint(50, 700), randint(50, 950), randint(200, 600), 20, (0, 150, 0)) # зелёного цвета rgb 0 150 0


while True:
    clock.tick(FPS)#делаем задержку

    for event in pygame.event.get():#если нажать QUIT -> exit
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()# смотрим какие клавиши нажаты

    for object in all_objects:#обновляем координаты всех объектов с помощью полиморфизма
        object.update(keys)
    screen.fill((255, 255, 255))# очищаем холст(каждые 60 милисекунд)
    for object in all_objects: 
        object.draw(screen)

    pygame.display.update()#заменяем старый холст на новый
