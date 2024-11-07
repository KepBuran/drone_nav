import random
from grid.grid import Grid


class GridDrawer: 
    def __init__(self, pygame, screen, draw_grid_lines=False):   
        self.pygame = pygame    
        self.screen = screen
        self.draw_grid_lines = draw_grid_lines

    def draw(self, grid: Grid, color=(0, 255, 0)):
        for x in range(0, grid.grid_width, grid.cell_size):
            for y in range(0, grid.grid_height, grid.cell_size):
                rect = self.pygame.Rect(x + grid.x_offset, y + grid.y_offset, grid.cell_size, grid.cell_size)
                cell_value = grid.grid[y // grid.cell_size][x // grid.cell_size]
                # Calculate opacity based on cell value (assuming cell value ranges from 1 to 100)
                opacity = min(int((cell_value / 100) * 255), 255)
                color_with_opacity = color + (opacity,)
                # Create a surface with per-pixel alpha
                cell_surface = self.pygame.Surface((grid.cell_size, grid.cell_size), self.pygame.SRCALPHA)
                cell_surface.fill(color_with_opacity)
                self.screen.blit(cell_surface, rect.topleft)

                # # Draw value in the cell
                # font = self.pygame.font.Font(None, 10)
                # text = font.render(str(cell_value), True, (40, 40, 0))
                # text_rect = text.get_rect(center=rect.center)
                # self.screen.blit(text, text_rect)


                # Draw the grid lines
                if self.draw_grid_lines:
                    self.pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
        # Draw grid borders
        self.pygame.draw.rect(self.screen, (200, 200, 200), (grid.x_offset, grid.y_offset, grid.grid_width, grid.grid_height), 1)

    def draw_clusters(self, grid: Grid, clusters_grid, clusters_amount):
        # Create a dictionary mapping each cluster index to a random color
        clusters_color = {i: (random.random() * 255, random.random() * 255, random.random() * 255) for i in range(clusters_amount)}

        for x in range(0, grid.grid_width, grid.cell_size):
            for y in range(0, grid.grid_height, grid.cell_size):
                rect = self.pygame.Rect(x + grid.x_offset, y + grid.y_offset, grid.cell_size, grid.cell_size)
                cluster = clusters_grid[y // grid.cell_size][x // grid.cell_size]
                color_with_opacity = clusters_color[cluster] + (255,)
                # Create a surface with per-pixel alpha
                cell_surface = self.pygame.Surface((grid.cell_size, grid.cell_size), self.pygame.SRCALPHA)
                cell_surface.fill(color_with_opacity)
                self.screen.blit(cell_surface, rect.topleft)

