import pygame
import sys

pygame.init()


WIDTH = 1540
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precision Platformer")

background_img = pygame.image.load("assets/green-background.png").convert()
background_img = pygame.transform.scale(
    background_img,
    (WIDTH, HEIGHT)
)

player_sheet = pygame.image.load("assets/Player Sprite Sheet.png").convert_alpha()

# Extract all sprite images from the sprite sheet
cooldown_img = player_sheet.subsurface((50, 430, 130, 160))
idle2_img = player_sheet.subsurface((200, 430, 130, 160))
idle1_img = player_sheet.subsurface((350, 430, 130, 160))
run2_img = player_sheet.subsurface((500, 430, 130, 160))
run3_img = player_sheet.subsurface((650, 430, 130, 160))
run4_img = player_sheet.subsurface((800, 430, 130, 160))

# Scale all sprite images to 50x60 pixels
cooldown_img = pygame.transform.scale(cooldown_img, (50, 60))
idle2_img = pygame.transform.scale(idle2_img, (50, 60))
idle1_img = pygame.transform.scale(idle1_img, (50, 60))
run2_img = pygame.transform.scale(run2_img, (50, 60))
run3_img = pygame.transform.scale(run3_img, (50, 60))
run4_img = pygame.transform.scale(run4_img, (50, 60))

Platform_sheet = pygame.image.load("assets/Platform Sprite Sheet.png").convert_alpha()

# Extract all platform images from the sprite sheet
platform1_img = Platform_sheet.subsurface((460, 305, 250, 145))
platform2_img = Platform_sheet.subsurface((0, 95, 380, 135))
platform3_img = Platform_sheet.subsurface((0, 305, 430, 125))
platform4_img = Platform_sheet.subsurface((790, 305, 530, 125))
platform5_img = Platform_sheet.subsurface((430, 95, 660, 120))
platform6_img = Platform_sheet.subsurface((0, 495, 1320, 165))

#Scale all platform images to their respective sizes
x1 = 100
y1 = 58
x2 = 152
y2 = 54
x3 = 172
y3 = 50
x4 = 212
y4 = 50
x5 = 264
y5 = 48
x6 = 528
y6 = 66
platform1_img = pygame.transform.scale(platform1_img, (x1, y1))
platform2_img = pygame.transform.scale(platform2_img, (x2, y2))
platform3_img = pygame.transform.scale(platform3_img, (x3, y3))
platform4_img = pygame.transform.scale(platform4_img, (x4, y4))
platform5_img = pygame.transform.scale(platform5_img, (x5, y5))
platform6_img = pygame.transform.scale(platform6_img, (x6, y6))

ground_img = pygame.image.load("assets/Ground Platform.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (1700, 300))

trophy_img = pygame.image.load("assets/Trophy.png").convert_alpha()
trophy_img = pygame.transform.scale(trophy_img, (50, 50))

clock = pygame.time.Clock()

GRAVITY = 0.5

camera_y = 0
reality = 0


class Player:

    def __init__(self):
        self.spawn()

    def spawn(self):
        self.rect = pygame.Rect(380, 500, 40, 60)

        self.vel_x = 0
        self.vel_y = 0

        self.speed = 5
        self.jump_power = -13

        self.on_ground = False

        self.can_dash = True

        self.facing = 1
        self.dash_timer = 0
        self.dash_up = False

        self.current_image = idle1_img
        self.animation_timer = 0

    def update(self):

        keys = pygame.key.get_pressed()

        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_up and self.dash_timer == 0:
                self.vel_y = -7
        else:
            self.dash_up = False
            self.vel_x = 0
            if keys[pygame.K_a]:
                self.vel_x = -self.speed
                self.facing = -1

            if keys[pygame.K_d]:
                self.vel_x = self.speed
                self.facing = 1
    
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = self.jump_power

        self.vel_y += GRAVITY

        self.rect.x += self.vel_x

        for platform in active_platforms() + [ground_rect] + [trophy_rect]:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right

        self.rect.y += self.vel_y

        self.on_ground = False

        for platform in active_platforms() + [ground_rect] + [trophy_rect]:

            if self.rect.colliderect(platform):

                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_dash = True

                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
        if not self.can_dash:

            self.current_image = cooldown_img

        elif self.vel_x != 0:

            self.animation_timer += 1

            frame = (self.animation_timer // 8) % 4

            if frame == 0:
                self.current_image = idle1_img

            elif frame == 1:
                self.current_image = run2_img

            elif frame == 2:
                self.current_image = run3_img

            else:
                self.current_image = run4_img

        elif self.on_ground and self.vel_x == 0:
            self.animation_timer += 1

            if (self.animation_timer // 30) % 2 == 0:
                self.current_image = idle1_img
            else:
                self.current_image = idle2_img
            
    def dash(self):

        if not self.can_dash:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.vel_y = -18
            self.vel_x = 0
            self.dash_up = True

        elif self.facing == -1:
            self.vel_x = -18
            self.vel_y = 0

        else:
            self.vel_x = 18
            self.vel_y = 0

        self.dash_timer = 10
        self.can_dash = False

player = Player()

trophy_rect = pygame.Rect(850, -2750, 50, 50)
ground_rect = pygame.Rect(0, 750, WIDTH, 50)

platforms = [

    (pygame.Rect(650, 625, x6, y6), 0, platform6_img),
    (pygame.Rect(1150, 500, x5, y5), 0, platform5_img),
    (pygame.Rect(650, 400, x5, y5), 0, platform5_img),

    (pygame.Rect(400, 300, x5, y5), 1, platform5_img),
    (pygame.Rect(600, 0, x4, y4), 1, platform4_img),
    (pygame.Rect(200, -120, x4, y4), 1, platform4_img),

    (pygame.Rect(700, -300, x3, y3), 0, platform3_img),
    (pygame.Rect(50, -300, x3, y3), 0, platform3_img),
    (pygame.Rect(350, -500, x3, y3), 1, platform3_img),
    
    (pygame.Rect(800, -525, x2, y2), 0, platform2_img),
    (pygame.Rect(550, -650, x3, y3), 0, platform3_img),
    (pygame.Rect(250, -900, x2, y2), 1, platform2_img),

    (pygame.Rect(625, -1100, x1, y1), 0, platform1_img),
    (pygame.Rect(400, -1300, x1, y1), 1, platform1_img),
    (pygame.Rect(100, -1500, x1, y1), 0, platform1_img),

    (pygame.Rect(400, -1700, x5, y5), 0, platform5_img),

    (pygame.Rect(725, -1800, x1, y1), 0, platform1_img),
    (pygame.Rect(1150, -1900, x1, y1), 1, platform1_img),
    (pygame.Rect(800, -2100, x1, y1), 0, platform1_img),

    (pygame.Rect(550, -2350, x3, y3), 0, platform3_img),
    (pygame.Rect(900, -2300, x1, y1), 1, platform1_img),
    (pygame.Rect(600, -2550, x1, y1), 0, platform1_img),
        
    (pygame.Rect(750, -2700, x4, y4), 1, platform4_img),

]

def active_platforms():

    return [
        rect
        for rect, state, img in platforms
        if state == reality
    ]


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_l:
                reality = 1 - reality

            if event.key == pygame.K_r:
                player.spawn()
                camera_y = 0

            if event.key == pygame.K_k:
                player.dash()

    player.update()

    target_camera = player.rect.centery - HEIGHT // 2

    if target_camera > 50:
        camera_y = 50
    else:
        camera_y = target_camera

    screen.blit(background_img, (0, 0))

    for rect, state, img in platforms:

        draw_rect = pygame.Rect(
            rect.x,
            rect.y - camera_y,
            rect.width,
            rect.height
        )

        if state == 0:
            color = (100, 220, 255)
        else:
            color = (255, 120, 180)

        if state == reality:
            screen.blit(img,(rect.x, rect.y - camera_y))
        else:
            if state == 0:
                pygame.draw.rect(
                screen,
                (28, 80, 184),
                (
                    rect.x,
                    rect.y - camera_y,
                    rect.width,
                    rect.height
                ),
                1
            )
            else:
                pygame.draw.rect(
                screen,
                (184, 39, 123),
                (
                    rect.x,
                    rect.y - camera_y,
                    rect.width,
                    rect.height
                ),
                1
            )

    screen.blit(ground_img, (ground_rect.x - 65, ground_rect.y -30 - camera_y))
    screen.blit(trophy_img, (trophy_rect.x, trophy_rect.y - camera_y))

    image = player.current_image

    if player.facing == -1:
        image = pygame.transform.flip(image, True, False)

    draw_x = player.rect.centerx - image.get_width() // 2

    if player.facing == 1:
        draw_x -= 5
    else:
        draw_x += 5

    screen.blit(image, (draw_x, player.rect.y - camera_y))
    
    pygame.display.update()

    clock.tick(60)