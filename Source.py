
import numpy as np
import random
import time
import heapq
from enum import Enum
from typing import List, Tuple, Dict, Set
import math
import pygame
import sys


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    TRAP = 2
    EXIT = 3
    LOCK = 4
    START = 5


class Colors:
    # Gender-neutral, psychologically appealing pastel and vibrant colors
    WHITE = (255, 255, 255)
    BLACK = (40, 40, 40)
    RED = (255, 99, 132)  # Vibrant but soft red
    GREEN = (102, 205, 170)  # Aquamarine (fresh, calming)
    BLUE = (100, 149, 237)  # Cornflower blue (friendly, neutral)
    YELLOW = (255, 221, 77)  # Warm yellow (cheerful, energetic)
    PURPLE = (186, 104, 200)  # Soft purple (creative, inviting)
    ORANGE = (255, 167, 38)  # Orange (fun, energetic)
    GRAY = (180, 180, 180)
    PATH = (255, 193, 7)  # Gold/yellow for path (visible, positive)
    SCIENTIST = (0, 191, 255)  # Deep sky blue (neutral, energetic)
    TEXT_BG = (240, 240, 255)  # Very light blue-purple
    BG = (245, 245, 245)  # Gentle off-white background
    HEART = (255, 99, 132)  # Red-pink for hearts
    STAR = (255, 221, 77)  # Gold for stars
    FLOWER = (255, 182, 193)  # Light pink for flower emoji
    TROPHY = (255, 215, 0)  # Trophy gold


class MazeGame:
    def __init__(self, size: int = 15):
        self.size = size
        self.maze = np.zeros((size, size), dtype=int)
        self.start_pos = None
        self.exit_pos = None
        self.trap_costs = {}
        self.cell_size = 40
        self.width = size * self.cell_size
        self.banner_height = 60
        self.height = size * self.cell_size + 200 + self.banner_height
        self.dynamic_change_probability = 0.1
        self.fps = 30

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Escape - Save the Scientist")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 24, bold=True)
        self.title_font = pygame.font.SysFont('Comic Sans MS', 36, bold=True)
        self.emoji_font = pygame.font.SysFont('Segoe UI Emoji', 32)

    def draw_banner(self):
        banner_rect = pygame.Rect(0, 0, self.width, self.banner_height)
        pygame.draw.rect(self.screen, Colors.BG, banner_rect, border_radius=20)
        title_surface = self.title_font.render('🌟 Maze Escape - Save the Scientist 🌟', True, Colors.BLUE)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.banner_height // 2))
        self.screen.blit(title_surface, title_rect)

    def draw_stats(self, stats: list):
        # Draw stats background
        stats_rect = pygame.Rect(0, self.size * self.cell_size + self.banner_height, self.width, 200)
        pygame.draw.rect(self.screen, Colors.TEXT_BG, stats_rect, border_radius=20)

        # Draw stats text
        y_offset = self.size * self.cell_size + self.banner_height + 20
        line_height = 32

        for text in stats:
            if 'successfully' in text or 'escaped' in text:
                emoji = '🏆'
                emoji_color = Colors.TROPHY
            elif 'Failed' in text or 'No path' in text:
                emoji = '💔'
                emoji_color = Colors.RED
            elif 'steps' in text or 'cost' in text:
                emoji = '⭐'
                emoji_color = Colors.STAR
            else:
                emoji = '🌼'
                emoji_color = Colors.FLOWER
            emoji_surface = self.emoji_font.render(emoji, True, emoji_color)
            self.screen.blit(emoji_surface, (10, y_offset - 4))
            text_surface = self.font.render(text, True, Colors.BLACK)
            text_rect = text_surface.get_rect(left=50, top=y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += line_height

    def wait_for_key(self):
        waiting = True
        text = self.font.render('Click or press any key to continue...', True, Colors.BLUE)
        text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Handle both keyboard and mouse clicks
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    # Clear event queue to prevent carrying over to next trial
                    pygame.event.clear()
                    return
            self.clock.tick(30)

    def generate_maze(self):
        # Reset maze
        self.maze.fill(CellType.EMPTY.value)
        self.trap_costs.clear()

        # Generate walls (30% of cells)
        wall_count = int(0.3 * self.size * self.size)
        wall_positions = random.sample([(i, j) for i in range(self.size) for j in range(self.size)], wall_count)
        for pos in wall_positions:
            self.maze[pos] = CellType.WALL.value

        # Generate traps (10% of cells)
        available_cells = [(i, j) for i in range(self.size) for j in range(self.size)
                           if self.maze[i, j] == CellType.EMPTY.value]
        trap_count = int(0.1 * self.size * self.size)
        trap_positions = random.sample(available_cells, trap_count)
        for pos in trap_positions:
            self.maze[pos] = CellType.TRAP.value
            self.trap_costs[pos] = random.randint(10, 20)

        # Generate locks (5% of cells)
        available_cells = [(i, j) for i in range(self.size) for j in range(self.size)
                           if self.maze[i, j] == CellType.EMPTY.value]
        lock_count = int(0.05 * self.size * self.size)
        lock_positions = random.sample(available_cells, lock_count)
        for pos in lock_positions:
            self.maze[pos] = CellType.LOCK.value

        # Set start and exit positions
        available_cells = [(i, j) for i in range(self.size) for j in range(self.size)
                           if self.maze[i, j] == CellType.EMPTY.value]
        self.start_pos, self.exit_pos = random.sample(available_cells, 2)
        self.maze[self.start_pos] = CellType.START.value
        self.maze[self.exit_pos] = CellType.EXIT.value

    def apply_dynamic_change(self):
        """Randomly modify the maze during execution"""
        if random.random() < self.dynamic_change_probability:
            available_cells = [(i, j) for i in range(self.size) for j in range(self.size)
                               if self.maze[i, j] == CellType.EMPTY.value]
            if available_cells:
                pos = random.choice(available_cells)
                change_type = random.choice([CellType.TRAP.value, CellType.LOCK.value])
                self.maze[pos] = change_type
                if change_type == CellType.TRAP.value:
                    self.trap_costs[pos] = random.randint(10, 20)
                return True, pos
        return False, None

    def draw_cell(self, x: int, y: int, cell_type: int, highlight: bool = False, is_scientist: bool = False):
        rect = pygame.Rect(y * self.cell_size, x * self.cell_size + self.banner_height, self.cell_size, self.cell_size)

        colors = {
            CellType.EMPTY.value: Colors.WHITE,
            CellType.WALL.value: Colors.PURPLE,
            CellType.TRAP.value: Colors.RED,
            CellType.EXIT.value: Colors.GREEN,
            CellType.LOCK.value: Colors.ORANGE,
            CellType.START.value: Colors.BLUE
        }

        color = colors.get(cell_type, Colors.WHITE)
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, Colors.GRAY, rect, 2, border_radius=12)

        if highlight:
            pygame.draw.rect(self.screen, Colors.PATH, rect, border_radius=12)
            # Add a glowing effect
            glow_rect = rect.inflate(8, 8)
            pygame.draw.rect(self.screen, Colors.PATH, glow_rect, 3, border_radius=16)

        if is_scientist:
            scientist_rect = pygame.Rect(y * self.cell_size + 8, x * self.cell_size + self.banner_height + 8,
                                         self.cell_size - 16, self.cell_size - 16)
            pygame.draw.ellipse(self.screen, Colors.SCIENTIST, scientist_rect)
            # Draw a star above the scientist (gender-neutral, achievement)
            star_surface = self.emoji_font.render('⭐', True, Colors.STAR)
            self.screen.blit(star_surface, (scientist_rect.centerx - 12, scientist_rect.top - 28))

    def draw_maze(self, path: List[Tuple[int, int]] = None, current_pos: Tuple[int, int] = None, stats: list = None):
        self.screen.fill(Colors.BG)
        self.draw_banner()

        for i in range(self.size):
            for j in range(self.size):
                is_scientist = (i, j) == current_pos
                self.draw_cell(i, j, self.maze[i, j], highlight=(path and (i, j) in path), is_scientist=is_scientist)

        if stats:
            self.draw_stats(stats)

        pygame.display.flip()

    def execute_path(self, path: List[Tuple[int, int]], planning_stats: dict) -> Tuple[bool, int, int]:
        if not path:
            return False, 0, 0

        total_cost = 0
        steps_taken = 0
        current_pos = path[0]
        current_path = path
        last_update_time = time.time()
        movement_delay = 0.1

        # Print initial path information to terminal
        print("\nPath Execution Started:")
        print("----------------------")
        print(f"Initial path length: {len(path)}")
        print(f"Start position: {self.start_pos}")
        print(f"Target exit: {self.exit_pos}")
        print("----------------------")

        while steps_taken < len(current_path):
            self.clock.tick(self.fps)

            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if current_time - last_update_time >= movement_delay:
                # Apply possible dynamic changes
                change_occurred, change_pos = self.apply_dynamic_change()

                if change_occurred and change_pos in current_path[steps_taken:]:
                    print(f"\nDynamic change detected at position {change_pos}!")
                    print("Replanning path from current position...")
                    new_path, new_steps, new_cost = self.a_star_search(start=current_pos)

                    if new_path:
                        print(f"New path found!")
                        print(f"New path length: {len(new_path)}")
                        print(f"Estimated new cost: {new_cost}")
                        current_path = new_path
                        steps_taken = 0
                        planning_stats.append(f"Path replanned: new length {len(new_path)}")
                    else:
                        print("No alternative path found after dynamic change!")
                        return False, steps_taken, total_cost

                current_pos = current_path[steps_taken]
                step_cost = self.get_cost(current_pos)
                total_cost += step_cost
                steps_taken += 1
                last_update_time = current_time

                # Print progress to terminal
                print(
                    f"\rStep {steps_taken}/{len(current_path)} | Current Position: {current_pos} | Step Cost: {step_cost} | Total Cost: {total_cost}",
                    end="")

                # Update stats display
                current_stats = planning_stats + [
                    f"Current steps: {steps_taken}",
                    f"Current cost: {total_cost}"
                ]
                self.draw_maze(current_path, current_pos, current_stats)

                if current_pos == self.exit_pos:
                    print("\n\nPath Execution Completed!")
                    print("------------------------")
                    print(f"Total steps taken: {steps_taken}")
                    print(f"Total path cost: {total_cost}")
                    return True, steps_taken, total_cost

        return False, steps_taken, total_cost

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.size and 0 <= new_y < self.size and
                    self.maze[new_x, new_y] != CellType.WALL.value):
                neighbors.append((new_x, new_y))
        return neighbors

    def get_cost(self, pos: Tuple[int, int]) -> int:
        if pos in self.trap_costs:
            return self.trap_costs[pos]
        return 1

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def a_star_search(self, start: Tuple[int, int] = None) -> Tuple[List[Tuple[int, int]], int, int]:
        if start is None:
            start = self.start_pos

        frontier = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, self.exit_pos)}

        explored = set()
        steps = 0

        while frontier:
            current_f, current = heapq.heappop(frontier)
            steps += 1

            if current == self.exit_pos:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

                return path, steps, g_score[self.exit_pos]

            explored.add(current)

            for neighbor in self.get_neighbors(current):
                if self.maze[neighbor] == CellType.LOCK.value and neighbor in explored:
                    continue

                tentative_g_score = g_score[current] + self.get_cost(neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_distance(neighbor, self.exit_pos)
                    if neighbor not in explored:
                        heapq.heappush(frontier, (f_score[neighbor], neighbor))

        return None, steps, 0


def run_simulation(num_trials: int = 3):
    game = MazeGame()

    try:
        for trial in range(num_trials):
            print(f"\n{'=' * 50}")
            print(f"Starting Trial {trial + 1} of {num_trials}")
            print(f"{'=' * 50}")

            game.generate_maze()

            # Initial stats
            planning_stats = [
                f"Trial {trial + 1} of {num_trials}",
                "----------------------------"
            ]
            game.draw_maze(stats=planning_stats)

            print("\nMaze Generated:")
            print(f"Size: {game.size}x{game.size}")
            print(f"Start Position: {game.start_pos}")
            print(f"Exit Position: {game.exit_pos}")

            # Find initial path using A*
            print("\nSearching for path using A*...")
            path, planning_steps, initial_cost = game.a_star_search()

            if path:
                print("\nA* Search Results:")
                print("------------------")
                print(f"Initial path found!")
                print(f"Planning steps taken: {planning_steps}")
                print(f"Estimated initial cost: {initial_cost}")
                print(f"Path length: {len(path)}")
                print(f"Path: {path}")
                print("------------------")

                # Update stats with path information
                planning_stats.extend([
                    "Initial path found!",
                    f"Planning steps: {planning_steps}",
                    f"Estimated cost: {initial_cost}",
                    f"Path length: {len(path)}"
                ])

                game.draw_maze(path, stats=planning_stats)

                # Execute path with possible dynamic changes
                success, total_steps, total_cost = game.execute_path(path, planning_stats)

                if success:
                    final_stats = planning_stats + [
                        "----------------------------",
                        "Scientist escaped successfully!",
                        f"Total steps taken: {total_steps}",
                        f"Total path cost: {total_cost}",
                        "----------------------------",
                        f"Time Complexity: O(E log V) where V={game.size * game.size}",
                        f"Space Complexity: O(V) where V={game.size * game.size}",
                        "----------------------------"
                    ]

                    print("\nFinal Results:")
                    print("--------------")
                    print("✓ Scientist escaped successfully!")
                    print(f"Final steps taken: {total_steps}")
                    print(f"Final path cost: {total_cost}")
                    print("\nComplexity Analysis:")
                    print(f"Time Complexity: O(E log V) where V={game.size * game.size} and E≈4V")
                    print(f"Space Complexity: O(V) where V={game.size * game.size}")
                    print("--------------")

                    if trial == num_trials - 1:
                        final_stats.append("Press any key to exit...")
                    else:
                        final_stats.append("Press any key for next trial...")
                else:
                    final_stats = planning_stats + [
                        "----------------------------",
                        "Failed to reach the exit!",
                        f"Steps taken: {total_steps}",
                        f"Path cost: {total_cost}",
                        "----------------------------"
                    ]

                    print("\nFinal Results:")
                    print("--------------")
                    print("✗ Failed to reach the exit!")
                    print(f"Steps taken before failure: {total_steps}")
                    print(f"Path cost before failure: {total_cost}")
                    print("--------------")

                    if trial == num_trials - 1:
                        final_stats.append("Press any key to exit...")
                    else:
                        final_stats.append("Press any key for next trial...")

                game.draw_maze(path, stats=final_stats)
                game.wait_for_key()
            else:
                print("\nNo initial path found to the exit!")
                print("Trial failed - maze may be unsolvable")

                planning_stats.extend([
                    "No path found!",
                    "----------------------------",
                    "Press any key to exit..." if trial == num_trials - 1 else "Press any key for next trial..."
                ])
                game.draw_maze(stats=planning_stats)
                game.wait_for_key()

            print(f"\n{'=' * 50}\n")

    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()

    finally:
        pygame.quit()


if __name__ == "__main__":
    print("\nMaze Escape - Save the Scientist")
    print("================================")
    print("Starting simulation with 3 trials...")
    run_simulation(3)
