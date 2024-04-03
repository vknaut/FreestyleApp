import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback, text_color = (0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.font = pygame.font.Font("./assets/Antonio-Regular.ttf", 22)
        self.text_color = text_color

    def draw(self, screen):
        current_color = self.color
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color

        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
