class Logger:
    def __init__(self, pygame, screen, grid, is_log_on_screen=True):
        self.grid = grid
        self.pygame = pygame
        self.screen = screen
        self.cells_sum_list = []
        self.is_log_on_screen = is_log_on_screen

    def log_on_screen(self, message, position):
        # Initialize font
        font = self.pygame.font.SysFont(None, 24)
        
        # Render the text
        text_surface = font.render(message, True, (255, 0, 0))
        
        # Get the text rectangle and position it
        text_rect = text_surface.get_rect(topright=position)
        
        # Blit the text to the screen
        self.screen.blit(text_surface, text_rect)

    def log_grid_sum(self):
        # Get the sum of the cells
        cells_sum = self.grid.get_cells_sum()

        self.cells_sum_list.append(cells_sum)
        
        # Log the sum on the screen
        if (self.is_log_on_screen):
            self.log_on_screen(f'Sum: {int(cells_sum)}', (self.screen.get_width() - 10, 10))

    def log_iteration(self, iterations):
        # Log the iteration count on the screen
        if (self.is_log_on_screen):
            self.log_on_screen(f'Iteration: {iterations}', (self.screen.get_width() - 10, 30))