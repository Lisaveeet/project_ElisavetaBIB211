import pygame


all_objects = [] # Создаём массив состоящий из всех объектов, чтобы обновлять их местоположение


class Object: # абстрактный объект
    def __init__(self, x, y, w, h, color=(0, 0, 0)): # вся игра построена на прямоугольниках
        """ Метод для присваивания каждому объекту его координат (высота, длина), а также цвета.
        x, y - координаты высоты положения фона (прямоугольника)
        w, h - координаты длины положения  фона (прямоугольника)
        color - rgb значение
        """
        global all_objects
        self.rect = pygame.rect.Rect(x, y, w, h) # pygame object для создания прямоугольного объекта на заданных координатах,заданных размеров
        # однако это не "отрисованный" объект, а тот объект с которым происходит взаимодействие
        self.image = pygame.Surface((w, h)) # занимается отрисовкой объекта
        self.color = color # устанавливаем цвет
        self.id = 'to_object'# для инициализации в дальнейшем,что это за объект используется id
        self.tags = [] # аналогично id
        self.alive = True # проверка на то что игра не закончилось,используется как "жизнь"
        all_objects.append(self) # добавляем наш объект в список всех объектов

    def __repr__(self):#
        """Печатаемое формальное представление объекта.
        """
        return f'{self.id} {(self.rect.x, self.rect.y)}'

    def update(self, *args):
        """Переопределено в каждом дочернем объекте.
        """
        global all_objects
        pass

    def draw(self, surface, *args): # занимется отрисовкой объекта. В данном случае просто рисует.
        """#Метод blit() применяется к той поверхности, на которую "накладывается", 
        т. е. на которой "отрисовывается", другая. 
        Другими словами, метод blit() применяется к родительской Surface, 
        в то время как дочерняя передается в качестве аргумента. 
        """
        self.image.fill(self.color)
        surface.blit(self.image, self.rect)


class Bullet(Object): # родительский объект
    def __init__(self, x, y, d, player_color):
        """ Вызываем родительский конструктор,
        выставляем направления движения пули, указывая, чья это была пуля.
       x, y - координаты положения объекта (пули)
       d - координаты направления объекта (пули)
       player_color - цвет объекта (пули)
        """
        super().__init__(x, y, 5, 5, (55, 55, 55)) 
        self.dir = d 
        self.player_color = player_color 
        self.id = 'to_bullet' # См Object
        self.tags += ['bullet']

    def update(self, *args):
        """Метод, который занимается обновлением координат пули.
        *args используется для передачи произвольного числа неименованных аргументов функции.
        """
        global all_objects
        if self.alive: # если игра ещё не закончена или пуля не врезалась в стену
            self.rect.move_ip(*self.dir) # pygame.Rect.move moves Двигает "пулю" в заданом направлении
            for object in all_objects: # бежим по всем объектам
                if 'tank' in object.tags: # провереям фигуры 
                    if self.player_color != object.color and self.rect.colliderect(object.rect): # если объект пули "наслоился" на вражеский танк
                        self.alive = False # убиваем себя и танк
                        object.alive = False
                elif 'wall' in object.tags: # если наслоились на стену, то пуля не должна двигаться и умирает
                    if self.rect.colliderect(object.rect):
                        self.alive = False



class DefaultTank(Object): # Объект фигуры "Танк"
    def __init__(self, x, y, d, color):
        """ Присваиваем клавиши для управления фигурами.
        x, y - координаты положения танка
        d - координаты направления движения танка
        color - rgb значение цвета танка
        """
        super().__init__(x, y, 55, 55, color)#Вызываем родительский конструктор
        self.dir = d # выставляем направление
        self.up = None # клавиши контроля движения
        self.down = None # клавиши контроля
        self.right = None# клавиши контроля
        self.left = None# клавиши контроля
        self.shoot = None # клавиши контроля выстрела
        self.shoot_cd = 30 # константное кол-во допустимых выстрелов
        self.prev_shoot = self.shoot_cd # кол-во оставшихся выстрелов данного танка
        self.id = 'to_deftank' # id - что это танк
        self.tags += ['tank'] # tag - что это танк
        self.alive = True # танк жив

    def set_controls(self, up, down, right, left, shoot):
        """ Функция, которая устанавливает клавиши контроля для каждой команды
        """
        self.up = up # вверх
        self.down = down # вниз
        self.right = right # вправо
        self.left = left # влево
        self.shoot = shoot b #стрелять

    def shot(self):
        """ Вызываем выстрел.
        """
        global all_objects
        if not self.prev_shoot: # если не ноль, то
            self.prev_shoot = self.shoot_cd # -1 меняем выстрелы у танка
            Bullet(self.rect.x + 25, self.rect.y + 25, (self.dir[0] * 2, self.dir[1] * 2), self.color) # создаёт новую пулю


    def update(self, *args):
        """ Функция обновления местоположения танка.
         *args используется для передачи произвольного числа неименованных аргументов функции.
         Обновляется каждое количество выстрелов, 
         проверяется, задел ли танк своего противника выстрелом; 
         проверяем два возможных исхода. 
         Если не задел, то игра продолжается и происходит обновление координат положения и направления движения танка и пулей
         
        """
        global all_objects
        self.prev_shoot = max(0, self.prev_shoot - 1) #обновляем кол-во выстрелов

        if self.alive: # если танк жив и игра ещё продолжается
            can_move_up = can_move_down = can_move_left = can_move_right = True
            upper_rect = pygame.rect.Rect((self.rect.x, self.rect.y - 1, self.rect.h, self.rect.w))
            lower_rect = pygame.rect.Rect((self.rect.x, self.rect.y + 1, self.rect.h, self.rect.w))
            righter_rect = pygame.rect.Rect((self.rect.x + 1, self.rect.y, self.rect.h, self.rect.w))
            lefter_rect = pygame.rect.Rect((self.rect.x - 1, self.rect.y, self.rect.h, self.rect.w))

            for object in all_objects: # танк не может пройти о стену, он ударяется о нее
                if ('tank' in object.tags or 'wall' in object.tags) and object != self:
                    can_move_up = can_move_up and not upper_rect.colliderect(object.rect)
                    can_move_down = can_move_down and not lower_rect.colliderect(object.rect)
                    can_move_right = can_move_right and not righter_rect.colliderect(object.rect)
                    can_move_left = can_move_left and not lefter_rect.colliderect(object.rect)

            keys = args[0] 
            """собственные перечисляемые свойства объектов (положение, цвет, все координаты) - возвращаются
            """
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
        """ Отрисовка направления движения и выстрелов танка.
         *args используется для передачи произвольного числа неименованных аргументов функции.
         Отрисовка выполняется с помощью метода blit()
         Surface - создает дополнительные поверхности, в случае наслаивания обхектов
        """
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


class DefaultWall(Object): # Объект стены
    def __init__(self, x, y, w, h, color=(0, 0, 0)): # аналагочно как и для вышеперечисленных объектов
        super().__init__(x, y, w, h, color)
        self.id = 'to_defwall'
        self.tags += ['wall']
