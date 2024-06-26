from constants import *
import pygame, random

class Drawable:
    def __init__(self, image_path, x, y):
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Movable(Drawable):
    def update(self, counter):
        pass

class Dog(Movable):
    def __init__(self, x, y):
        super().__init__(DOG_IMAGE_PATH, x, y)
        self.anime = False
        self.direction = "UP"

    def update(self, counter):
        if self.anime:
            if self.direction == "UP":
                if counter % 5 == 0:
                    self.y -= 20
                if counter % 7 == 0:
                    self.y += 10
                if self.rect.top <= HEIGHT - 130:
                    self.direction = "DOWN"
            elif self.direction == "DOWN":
                if counter % 5 == 0:
                    self.y += 20
                if counter % 7 == 0:
                    self.y -= 10
                if self.rect.top > HEIGHT:
                    self.anime = False
                    self.y = HEIGHT + 130
                    self.direction = "UP"
            self.rect = self.surf.get_rect(center=(self.x, self.y))

    def start_animation(self):
        self.anime = True

class Bird(Drawable):
    def __init__(self, x, y):
        super().__init__(BIRD_IMAGE_PATH, x, y)

    def reposition(self):
        self.rect = self.surf.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

class Crosshair(Drawable):
    def update_position(self, pos):
        self.rect = self.surf.get_rect(center=pos)

class Ammo:
    def __init__(self, ammo_images):
        self.ammo_images = ammo_images
        self.ammo = 4
        self.rect = self.ammo_images[self.ammo].get_rect(bottomleft=(5, HEIGHT - 5))
        self.reload_started = False

    def draw(self, screen):
        screen.blit(self.ammo_images[self.ammo], self.rect)

    def decrease(self):
        if self.ammo > 0:
            self.ammo -= 1

    def reload(self):
        self.ammo = 4
        self.reload_started = False

    def start_reload(self):
        self.reload_started = True

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Bird Hunting")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.clock = pygame.time.Clock()
        self.running = True
        self.counter = 0
        self.points = 0
        self.dog = Dog(WIDTH / 2, HEIGHT + 130)
        self.bird = Bird(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        self.crosshair = Crosshair(CROSSHAIR_IMAGE_PATH, WIDTH / 2, HEIGHT / 2)
        self.ammo = Ammo([pygame.image.load(path).convert_alpha() for path in AMMO_IMAGES_PATHS])
        self.font = pygame.font.SysFont('arial', 30, bold=True, italic=False)
        self.update_text()
    
    def update_text(self):
        self.text = "POINTS: " + str(self.points)
        self.text_surf = self.font.render(self.text, True, FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(topright=(WIDTH - 10, 10))

    def run(self):
        while self.running:
            self.counter += 1
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.crosshair.update_position(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ammo.ammo > 0:
                self.handle_shot(event.pos)

    def handle_shot(self, pos):
        self.ammo.decrease()
        self.sound_manager.play_shot()
        if self.bird.rect.collidepoint(pos):
            self.points += 1
            self.update_text()
            self.bird.reposition()

    def update_game_state(self):
        if self.ammo.ammo == 0 and not self.ammo.reload_started:
            self.sound_manager.play_reload()
            self.ammo.start_reload()
            self.dog.start_animation()
        if self.ammo.reload_started and self.counter % 200 == 0:
            self.ammo.reload()
        self.dog.update(self.counter)

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        self.ammo.draw(self.screen)
        self.bird.draw(self.screen)
        self.dog.draw(self.screen)
        self.screen.blit(self.text_surf, self.text_rect)
        self.crosshair.draw(self.screen)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()