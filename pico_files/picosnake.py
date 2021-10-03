from game import Game, GameObject, Cons
from game_objects import Snake, ScoreBoard, Apple
from graphics import Graphics, Shapes
import random as rnd

import math

class SnakeGame(Game):
    def __init__(self):
        super().__init__()
        self.score = 0

    def init(self):
        self.sb = ScoreBoard(30, 20)
        self.add_object(self.sb)
        self.snake = Snake(100, 100, col=self.rand_col())
        self.add_object(self.snake)

        self.add_object(Apple(rnd.randrange(0, Cons.WIDTH - 30), rnd.randrange(0, Cons.HEIGHT - 30), self.rand_col()))

    def rand_col(self):
        col_idx = len(Cons.FUN_COLS)
        return Cons.FUN_COLS[rnd.randrange(0, col_idx)]

    def update(self):
        self.snake.facing = 360-self.left_stick
        self.snake.speed = 30*(1-(self.right_stick/360))
        # if self.pressed('Left'):
        #     self.snake.facing_delta += self.snake.turnrate
        # if self.pressed('Right'):
        #     self.snake.facing_delta -= self.snake.turnrate
        # if self.pressed('Up'):
        #     self.snake.speed += self.snake.speedrate
        # if self.pressed('Down'):
        #     self.snake.speed -= self.snake.speedrate

        super().update()

        self.sb.set_speed(self.snake.speed)
        self.sb.set_score(self.score)
        self.sb.set_fps(self.fps)

        for obj in self.game_objects:
            if isinstance(obj, Apple):
                if(Shapes.contains(obj.hitpoly, (self.snake.x,self.snake.y))):
                    obj.remove = True
                    self.add_object(Apple(rnd.randrange(0, Cons.WIDTH - 30), rnd.randrange(0, Cons.HEIGHT - 30), self.rand_col()))
                    self.snake.feed(1, obj.col)
                    self.score += 1

    def draw(self):
        super().draw()

def main():
    game = SnakeGame()
    game.init()
    game.run()

if __name__ == '__main__':
    main()
