import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback, text_color=(0, 0, 0), image_path=None, hover_image_path=None, click_image_path=None, onclick_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.onclick_color = onclick_color  # Store the onclick color
        self.callback = callback
        self.font = pygame.font.Font("FreestyleApp/assets/Antonio-Regular.ttf", 22)
        self.text_color = text_color
        # Load images if paths are provided
        self.image = self.load_image(image_path) if image_path else None
        self.hover_image = self.load_image(hover_image_path) if hover_image_path else None
        self.click_image = self.load_image(click_image_path) if click_image_path else None
        self.is_clicked = False  # Track click state

    def load_image(self, path):
        try:
            return pygame.transform.scale(pygame.image.load(path), (self.rect.width, self.rect.height))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_clicked and self.click_image:
            # Draw click image if button is clicked
            screen.blit(self.click_image, self.rect.topleft)
        elif self.rect.collidepoint(mouse_pos) and self.hover_image:
            # Draw hover image if mouse is over the button
            screen.blit(self.hover_image, self.rect.topleft)
        elif self.image:
            # Draw normal image
            screen.blit(self.image, self.rect.topleft)
        else:
            # Use onclick_color if the button is clicked, otherwise use hover_color or normal color
            if self.is_clicked and self.onclick_color:
                current_color = self.onclick_color
            elif self.rect.collidepoint(mouse_pos):
                current_color = self.hover_color
            else:
                current_color = self.color
            pygame.draw.rect(screen, current_color, self.rect)

        # Always draw the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True  # Set click state to True when button is clicked
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.is_clicked:
                # Only call the callback if the mouse is released over the button after a click
                self.callback()
            self.is_clicked = False  # Reset click state on mouse release
