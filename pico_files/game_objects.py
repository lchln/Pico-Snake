from game import GameObject, Cons
from graphics import Shapes
import math

class Apple(GameObject):
    def __init__(self, x, y, c):
        super().__init__()
        self.x = x
        self.y = y
        self.r = 10
        self.col = c
        self.hitpoly = [
            (self.x-(self.r*1.5), self.y-(self.r*1.5)),
            (self.x+(self.r*1.5), self.y-(self.r*1.5)),
            (self.x+(self.r*1.5), self.y+(self.r*1.5)),
            (self.x-(self.r*1.5), self.y+(self.r*1.5))
        ]

    def draw(self, gfx):
        gfx.fill_rect(self.x, self.y, self.r, self.r, self.col)
        super().draw(gfx)

class Snake(GameObject):
    def __init__(self, x=(Cons.WIDTH/2), y=(Cons.HEIGHT/2), w=10, col=Cons.PINK):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.facing = 0
        self.dx = 0
        self.dy = 0
        self.col = col

        self.l = 1
        self.x_hist = []
        self.y_hist = []
        self.body_col = []

        self.body_gap = 2

        self.speed = 2

        for bp in range(self.l):
            self.x_hist.append(self.x)
            self.y_hist.append(self.y)
            self.body_col.append(self.col)

    def feed(self, food_amount, food_col):
        self.l += food_amount
        for bp in range(food_amount):
            self.body_col.append(food_col)

    def update(self):
        super().update()
        self.x += self.speed * math.sin(math.radians(self.facing))
        self.y += self.speed * math.cos(math.radians(self.facing))

        self.x_hist.insert(0, self.x)
        if(len(self.x_hist) > (self.l * self.body_gap)):
            self.x_hist.pop(-1)
        self.y_hist.insert(0, self.y)
        if(len(self.y_hist) > (self.l * self.body_gap)):
            self.y_hist.pop(-1)

        if self.x < 0 - self.w:
            self.x = Cons.WIDTH + self.w
        if self.y < 0 - self.w:
            self.y = Cons.HEIGHT + self.w
        if self.x > Cons.WIDTH + self.w:
            self.x = 0
        if self.y > Cons.HEIGHT + self.w:
            self.y = 0

        self.hitpoly = []
        self.headpoly = []

    def draw(self, gfx):
        # SPINE
        gfx.fill_rect(int(self.x), int(self.y), self.w - 5, self.w - 5, self.col)
        spine = []

        for bp in range(self.l):
            try:
                draw_x = int(self.x_hist[(bp + 1) * self.body_gap])
                draw_y = int(self.y_hist[(bp + 1) * self.body_gap])
            except:
                draw_x = int(self.x_hist[-1])
                draw_y = int(self.y_hist[-1])
            spine.append((draw_x, draw_y))

        for vtb in range(len(spine)-1):
            v0_x, v0_y = spine[vtb]
            v1_x, v1_y = spine[vtb+1]

            if abs(v1_x - v0_x) < 100 and abs(v1_y - v0_y) < 100:
                gfx.line(v0_x, v0_y, v1_x, v1_y, self.body_col[vtb])

        ## RECTS
        #     gfx.fill_rect(draw_x, draw_y, self.w, self.w, self.body_col[bp])
        # gfx.fill_rect(int(self.x), int(self.y), self.w + 5, self.w + 5, self.col)

        # for bp in range(self.l):
        #     try:
        #         draw_x = int(self.x_hist[(bp + 1) * self.body_gap])
        #         draw_y = int(self.y_hist[(bp + 1) * self.body_gap])
        #     except:
        #         draw_x = int(self.x_hist[-1])
        #         draw_y = int(self.y_hist[-1])

        #     gfx.fill_rect(draw_x, draw_y, self.w, self.w, self.body_col[bp])
        super().draw(gfx)

class ScoreBoard(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.score = 0
        self.speed = 0
        self.fps = 0

    def update(self):
        super().update()

    def draw(self, gfx):
        gfx.base_text('Score: ' + str(self.score), self.x, self.y, Cons.WHITE)
        gfx.base_text('Speed: ' + str(round(self.speed, 2)), self.x + 85, self.y, Cons.WHITE)
        gfx.base_text('FPS: '   + str(self.fps), self.x + 200, self.y, Cons.WHITE)

    def set_score(self, score):
        self.score = score

    def set_speed(self, speed):
        self.speed = speed

    def set_fps(self, fps):
        self.fps = fps
