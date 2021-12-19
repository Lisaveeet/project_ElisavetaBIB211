import pygame


all_objects = []# Создаём массив состоящий из всех объектов, чтобы обновлять из местоположение


class Object:#P.s это абстрактный объект
    def __init__(self, x, y, w, h, color=(0, 0, 0)):# вся игра построена на прямоугольниках
        #поэтому каждый объкт должен иметь его координаты:высоту,длину; и цвет.
        global all_objects
        self.rect = pygame.rect.Rect(x, y, w, h)#pygame object для создания прямоугольного объекта на заданных координатах,заданных размеров
        #однако это не "отрисованный" объект.а тот объект с которым происходит взаимодействие
        self.image = pygame.Surface((w, h))#занимается отрисовкой объекта
        self.color = color#устанавливаем цвет
        self.id = 'to_object'#Для инициализации в дальнейшем,что это за объект используется id. (мб удалить?)
        self.tags = [] #аналогично id
        self.alive = True #проверка на то что игра не закончилось,используется как "жизнь" в танках
        all_objects.append(self) #добавляем наш объект в список всех объектов

    def __repr__(self):#печатаемое формальное представление объекта.
        return f'{self.id} {(self.rect.x, self.rect.y)}'

    def update(self, *args):# переопределено в каждом дочернем объекте
        global all_objects
        pass

    def draw(self, surface, *args):#занимется отрисовкой объекта.В данном случае просто рисует 
        self.image.fill(self.color)
        surface.blit(self.image, self.rect)#Метод blit() применяется к той поверхности, на которую "накладывается", т. е. на которой "отрисовывается", другая. Другими словами, метод blit() применяется к родительской Surface, в то время как дочерняя передается в качестве аргумента. 


class Bullet(Object):
    def __init__(self, x, y, d, player_color):
        super().__init__(x, y, 5, 5, (55, 55, 55))#вызываем родительский конструктор
        self.dir = d# выставляем направление движение пули
        self.player_color = player_color # выставляем чья это была пуля
        self.id = 'to_bullet' # См Object
        self.tags += ['bullet']

    def update(self, *args):#занимается обновлением координат пули
        global all_objects
        if self.alive:# если игра ещё не закончена или пуля не врезалась в стену
            self.rect.move_ip(*self.dir) #pygame.Rect.move moves Двигает "пулю" в заданом направлении
            for object in all_objects:#бежим по всем объектам
                if 'tank' in object.tags:#проверем танки 
                    if self.player_color != object.color and self.rect.colliderect(object.rect):#если объект пули "наслоился" на вражеский танк
                        #то надо End Game бахнуть
                        #туть
                        self.alive = False#убиваем себя и танк
                        object.alive = False
                elif 'wall' in object.tags:#если наслоились на стену,то пуля не должна двигаться и умирает
                    if self.rect.colliderect(object.rect):
                        self.alive = False



class DefaultTank(Object):#Объект Танка
    def __init__(self, x, y, d, color):
        super().__init__(x, y, 55, 55, color)#Вызываем родительский конструктор
        self.dir = d # выставляем направление
        self.up = None # клавиши контроля движения
        self.down = None # клавиши контроля
        self.right = None# клавиши контроля
        self.left = None# клавиши контроля
        self.shoot = None # клавиши контроля выстрела
        self.shoot_cd = 30 # константное кол-во допустимых выстрелов
        self.prev_shoot = self.shoot_cd # кол-во оставшихся выстрелов данного танка
        self.id = 'to_deftank' # id что это танк
        self.tags += ['tank'] # tag что это танк
        self.alive = True #по дефолту танк жив

    def set_controls(self, up, down, right, left, shoot):#устанавливаем клавиши контроля
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.shoot = shoot

    def shot(self):#выстрел
        global all_objects
        if not self.prev_shoot:#если не ноль то
            self.prev_shoot = self.shoot_cd #-1 меняем выстрелы у танка
            bullet = Bullet(self.rect.x + 25, self.rect.y + 25, (self.dir[0] * 2, self.dir[1] * 2), self.color)# создаёп новую пулю
            all_objects.append(bullet)# добавляем пулю в список всех объектов

    def update(self, *args):# функция обновления местоположения танка
        global all_objects
        self.prev_shoot = max(0, self.prev_shoot - 1) # если обновляем кол-во выстрелов

        if self.alive:#если танк жив и игра ещё
            can_move_up = can_move_down = can_move_left = can_move_right = True
            upper_rect = pygame.rect.Rect((self.rect.x, self.rect.y - 1, self.rect.h, self.rect.w))
            lower_rect = pygame.rect.Rect((self.rect.x, self.rect.y + 1, self.rect.h, self.rect.w))
            righter_rect = pygame.rect.Rect((self.rect.x + 1, self.rect.y, self.rect.h, self.rect.w))
            lefter_rect = pygame.rect.Rect((self.rect.x - 1, self.rect.y, self.rect.h, self.rect.w))

            for object in all_objects:
                if ('tank' in object.tags or 'wall' in object.tags) and object != self:
                    can_move_up = can_move_up and not upper_rect.colliderect(object.rect)
                    can_move_down = can_move_down and not lower_rect.colliderect(object.rect)
                    can_move_right = can_move_right and not righter_rect.colliderect(object.rect)
                    can_move_left = can_move_left and not lefter_rect.colliderect(object.rect)

            keys = args[0]
            if all([self.up, self.down, self.right, self.left, self.shoot]):
                if keys[self.up]:
                    if can_move_up:
                        self.rect.move_ip(0, -1)
                    self.dir = (0, -1)
                elif keys[self.down]:
                    if can_move_down:
                        self.rect.move_ip(0, 1)
                    self.dir = (0, 1)
                elif keys[self.left]:
                    if can_move_left:
                        self.rect.move_ip(-1, 0)
                    self.dir = (-1, 0)
                elif keys[self.right]:
                    if can_move_right:
                        self.rect.move_ip(1, 0)
                    self.dir = (1, 0)

                if keys[self.shoot]:
                    self.shot()
            else:
                raise Exception(f'Не установлено управление для {(self.rect.x, self.rect.y)}')

    def draw(self, surface, *args):
        self.image.fill(self.color)
        surface.blit(self.image, self.rect)
        if self.dir == (0, -1):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 10, 15, 25))
        elif self.dir == (0, 1):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 20, 15, 25))
        elif self.dir == (-1, 0):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 10, self.rect.y + 20, 25, 15))
        elif self.dir == (1, 0):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 20, 25, 15))


class DefaultWall(Object):
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        super().__init__(x, y, w, h, color)
        self.id = 'to_defwall'
        self.tags += ['wall']
