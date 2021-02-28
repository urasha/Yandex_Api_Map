import pygame
from obj_coord import get_coords
from map_spn import get_spn

pygame.init()
pygame.font.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

screen = pygame.display.set_mode((600, 450))


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def start_menu():
    input_box1 = InputBox(200, 160, 140, 32)
    input_boxes = [input_box1]
    is_running = False

    search = FONT.render('Введите название объекта и нажмите Enter', 1, 'green')
    cancel = FONT.render('Для сброса - Escape', 1, 'green')

    while not is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_box1.text:
                        try:
                            ll, top = get_coords(input_box1.text)
                            return ll, get_spn(top)
                        except Exception:
                            input_box1.text = 'Ошибка'
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        screen.blit(search, (70, 70))
        screen.blit(cancel, (70, 100))

        pygame.display.flip()
