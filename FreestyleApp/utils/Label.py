class Label:
    def __init__(self, text, font, color, pos, line_spacing=5):
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.line_spacing = line_spacing
        self.lines = text.split('\n')  # Split the text into lines

    def update_text(self, new_text):
        self.text = new_text
        self.lines = new_text.split('\n')

    def draw(self, screen):
        x, y = self.pos
        for line in self.lines:
            text_surface = self.font.render(line, True, self.color)
            screen.blit(text_surface, (x, y))
            y += self.font.get_linesize() + self.line_spacing
