import pygame
from pygame.locals import *
import buttons

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')


font = pygame.font.SysFont('Roboto', 30)

# define colors
bg = (142, 135, 123)
block1 = (144, 180, 242)
block2 = (70, 131, 238)
block3 = (22, 99, 233)
paddle_col = (49, 115, 201)
paddle_outline = (44, 109, 193)
ball_col = (44, 59, 193)
ball_outline = (44, 56, 185)
text_col = (78, 81, 139)

# game variables
cols = 8
rows = 9
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

# buttons
game_state = "main"

breakout_title = pygame.image.load("breakout.jpeg").convert_alpha()
play_img = pygame.image.load("play.jpeg").convert_alpha()
quit_img = pygame.image.load("quit.jpeg").convert_alpha()

breakout_title = pygame.transform.scale(breakout_title, (350, 100))
play_button = buttons.Button(125, 250, play_img, 5)
quit_button = buttons.Button(325, 250, quit_img, 5)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# brick wall
class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 35

    def create_wall(self):
        self.blocks = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 3:
                    strength = 3
                elif row < 6:
                    strength = 2
                elif row < 9:
                    strength = 1

                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_col = block3
                elif block[1] == 2:
                    block_col = block2
                elif block[1] == 1:
                    block_col = block1
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)


class paddle():
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width / 6)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        collision_thresh = 5

        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1

        # wall collision
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # top or bot collision
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # paddle collision
        if self.rect.colliderect(player_paddle):
            # check top collision
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, ball_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, ball_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0


wall = wall()
wall.create_wall()
player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:
    clock.tick(fps)
    screen.fill(bg)

    if game_state == "main":
        screen.blit(breakout_title, (135, 100))
        if play_button.draw(screen):
            game_state = "play"
        if quit_button.draw(screen):
            run = False

    if game_state == "play":
        wall.draw_wall()
        player_paddle.draw()
        ball.draw()

    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    if not live_ball:
        if game_over == 0:
            if play_button.draw(screen):
                game_state = "play"
            if quit_button.draw(screen):
                run = False
        elif game_over == 1:
            draw_text('YOU WON!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 150, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 150, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()
