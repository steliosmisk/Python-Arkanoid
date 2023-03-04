import pygame

# Colors
LIGHT_BLUE = (200, 255, 255)

# Display
pygame.init()
screen = pygame.display.set_mode((500, 500))
screen.fill(LIGHT_BLUE)
clock = pygame.time.Clock()


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = LIGHT_BLUE
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(screen, self.fill_color, self.rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Creating a ball
ball = Picture('ball.png', 160, 200, 50, 50)

# Creating the Platform
platform_x = 200
platform_y = 410
platform = Picture('platform.png', platform_x, platform_y, 100, 30)

# Creating enemies
start_x = 5
start_y = 5
count = 9

monsters = []
for enemy in range(3):
    y = start_y + (55 * enemy)
    x = start_x + (27.5 * enemy)
    for _ in range(count):
        enemies = Picture('enemy.png', x, y, 50, 50)
        monsters.append(enemies)
        x += 55
    count -= 1

move_right = False
move_left = False
dx = 5
dy = 5

game_over = False
while not game_over:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *= (-1)

    if ball.rect.x < 0 or ball.rect.x > 450:
        dx *= (-1)

    if ball.rect.colliderect(platform.rect):
        dy *= (-1)

    if move_right:
        platform.rect.x += 5
    elif move_left:
        platform.rect.x -= 5

    if ball.rect.y > platform.rect.y + 20:
        image = pygame.font.SysFont('verdana', 60).render('YOU LOSE', True, (255, 0, 0))
        screen.blit(image, (170, 170))
        game_over = True

    if not monsters:
        image = pygame.font.SysFont('verdana', 60).render('YOU WIN', True, (0, 255, 0))
        screen.blit(image, (170, 170))
        game_over = True

    for j in monsters:
        j.draw()
        if j.rect.colliderect(ball.rect):
            monsters.remove(j)
            j.fill()
            dy *= (-1)

    platform.draw()
   
