import tkinter as tk
import random

# Розміри поля
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20

# Напрямки руху
DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змійка")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.reset_game()

        # Прив'язка клавіш
        self.root.bind("<KeyPress>", self.change_direction)

        self.game_loop()

    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]  # Початкова позиція
        self.direction = "Right"
        self.food = None
        self.spawn_food()
        self.game_over = False

    def spawn_food(self):
        while True:
            x = random.randint(0, WIDTH // CELL_SIZE - 1)
            y = random.randint(0, HEIGHT // CELL_SIZE - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        new_direction = event.keysym
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction in DIRECTIONS and new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = DIRECTIONS[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # Перевірка на зіткнення зі стіною або з тілом
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= WIDTH // CELL_SIZE or
            new_head[1] < 0 or new_head[1] >= HEIGHT // CELL_SIZE):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.spawn_food()
        else:
            self.snake.pop()

    def draw_elements(self):
        self.canvas.delete("all")

        # Малюємо змійку
        for (x, y) in self.snake:
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill="green"
            )

        # Малюємо їжу
        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL_SIZE, fy * CELL_SIZE,
            (fx + 1) * CELL_SIZE, (fy + 1) * CELL_SIZE,
            fill="red"
        )

    def game_loop(self):
        if not self.game_over:
            self.move_snake()
            self.draw_elements()
            self.root.after(100, self.game_loop)
        else:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, fill="white",
                                    font=("Arial", 24), text="Гра закінчена!")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
